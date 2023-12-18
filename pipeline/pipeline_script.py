#!/usr/bin/env python3
import os
import sys
import time
from datetime import datetime
from pyspark.sql import SparkSession
from Bio import SeqIO
from pipeline_argparser import argparser
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pipeline.constants import HH_SUITE__BIN_PATH, PDB70_PATH, S4PRED_PATH, ROOT_DIR
from pipeline.worker_task import check_if_already_ran, run_s4pred, read_horiz, run_hhsearch, run_parser, update_sequence_database, update_db_status, clean_up_tmp_files
from pipeline.master_task import merge_results, write_best_hits, write_profile_csv, save_results_to_db, get_avg_score_gmean, get_avg_score_std, zip_results
import zipfile
from pipeline.database import create_session
from pipeline.models.protein_results import ProteinResults, PENDING
from pipeline.models.pipeline_run_summary import PipelineRunSummary, SUCCESS, RUNNING, FAILED
from pipeline.models.proteome import Proteomes
from pipeline.logger import logger

def zip_module():
    """
    Function to zip the module for spark to use
    """
    path_to_zip = os.path.join(os.path.dirname(__file__), "..", "pipeline.zip")
    zipf = zipfile.ZipFile(path_to_zip, 'w', zipfile.ZIP_DEFLATED)
    exclude_folders = ['venv', 'ansible']

    for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), "..")):
        dirs[:] = [d for d in dirs if d not in exclude_folders]

        for file in files:
            if file.endswith('.py') or file.endswith('.env'):
                zipf.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), start=os.path.join(os.path.dirname(__file__), "..")))
    zipf.close()

    return path_to_zip


"""
usage: python pipeline_script.py INPUT.fasta  
approx 5min per analysis
"""
def read_input(file):
    """
    Function reads a fasta formatted file of protein sequences
    """
    logger.info("READING FASTA FILES")
    sequences = {}
    ids = []
    for record in SeqIO.parse(file, "fasta"):
        sequences[record.id] = record.seq
        ids.append(record.id)
    return(sequences)


def process_sequence(identifier, sequence, run_id, index):
    logger.info(f"PROCESSING SEQUENCE {index} with id {identifier}")
    tmp_file = f"{ROOT_DIR}/tmp/{run_id}/{index}.fas"
    horiz_file = f"{ROOT_DIR}/tmp/{run_id}/horiz/{index}.horiz"
    a3m_file = f"{ROOT_DIR}/tmp/{run_id}/a3m/{index}.a3m"
    hhr_file = f"{ROOT_DIR}/tmp/{run_id}/a3m/{index}.hhr"
    object_name = f"{run_id}/{index}.out"
    output_file = f"{ROOT_DIR}/data/output/{run_id}/{index}.out"

    # Early exit if the folders are not set up correctly
    if not os.path.exists(HH_SUITE__BIN_PATH):
        logger.error("Folder HH_SUITE__BIN_PATH does not exists: ", HH_SUITE__BIN_PATH)
        sys.exit(1)
    if not os.path.exists(PDB70_PATH+"_cs219.ffdata"):
        logger.error("Folder PDB70_PATH does not exists: ", PDB70_PATH)
        sys.exit(1)
    if not os.path.exists(S4PRED_PATH):
        logger.error("Folder S4PRED_PATH does not exists: ", S4PRED_PATH)
        sys.exit(1)
    
    os.makedirs(os.path.dirname(tmp_file), exist_ok=True)
    os.makedirs(os.path.dirname(horiz_file), exist_ok=True)
    os.makedirs(os.path.dirname(a3m_file), exist_ok=True)  

    has_already_run = check_if_already_ran(identifier, run_id)
    if has_already_run:
        logger.info(f"Sequence {identifier} has already been run")
        return
        
    with open(tmp_file, "w") as fh_out:
        fh_out.write(f">{identifier}\n")
        fh_out.write(f"{sequence}\n")
    try:
        update_db_status(run_id, identifier, RUNNING)
        run_s4pred(tmp_file, horiz_file)
        read_horiz(tmp_file, horiz_file, a3m_file)
        run_hhsearch(a3m_file)
        run_parser(hhr_file, output_file)
        update_sequence_database(output_file, run_id, identifier)
        update_db_status(run_id, identifier, SUCCESS)
        clean_up_tmp_files(tmp_file, horiz_file, a3m_file, hhr_file)
    except Exception as e:
        logger.error(e)
        update_db_status(run_id, identifier, FAILED)
        pass




if __name__ == "__main__":
    # unique random id for this run time in order to avoid conflicts
    num_workers = None
    spark = None
    master_url = None
    run_id = None

    args = argparser()
    if args.master:
        master_url = args.master
    if args.local:
        logger.info("RUNNING LOCALLY")
        master_url = "local[*]"
    if args.run_id:
        run_id = args.run_id
    if args.num_workers:
        num_workers = args.num_workers

    logger.debug('url:'+master_url)
    if not (master_url or args.local):
        logger.error("Please set the spark master with --master or run locally with --local")
        sys.exit(1)

    if master_url == "local[*]":
        num_workers = 1
    
    
    spark = SparkSession.builder.appName(run_id).master(master_url).getOrCreate()
    path_to_pipeline_zip = zip_module()
    spark.sparkContext.addPyFile(path_to_pipeline_zip)
    
    os.makedirs(f"{ROOT_DIR}/data/output/{run_id}", exist_ok=True)
    
    logger.info(f"SPARK SESSION STARTED on {master_url}")
    logger.info(f"START RUN ID: {run_id}")
    start_time = time.time()

    whoami = os.getenv('USER')
    session = create_session()

    pipeline_already_exists = session.query(PipelineRunSummary).filter(PipelineRunSummary.run_id == run_id).first()
    sequence_list = []
    if pipeline_already_exists is None:
        new_pipeline_run_summary = PipelineRunSummary(
            run_id=run_id,
            status=RUNNING,
            date_started=datetime.now(),
            author=whoami
        )
        session.add(new_pipeline_run_summary)
        session.commit()

        sequences = read_input(args.input_file)
        sequence_list = list(sequences.items())

        for sequence in sequence_list:
            id = sequence[0]
            seq = sequence[1]
            new_protein_results = ProteinResults(
                run_id=run_id,
                query_id=id,
                status=PENDING
            )
            session.add(new_protein_results)
    else:
        logger.info(f"Pipeline {run_id} already exists, re-running failed and pending sequences")
        all_not_success = session.query(ProteinResults).filter(ProteinResults.run_id == run_id).filter(ProteinResults.status != SUCCESS).all()
        for protein_result in all_not_success:
            if protein_result.status == FAILED:
                logger.info(f"Sequence {protein_result.query_id} failed, re-running")
            protein_result.status = PENDING
            session.add(protein_result)
            
        update_pipeline_run_summary = session.query(PipelineRunSummary).filter(PipelineRunSummary.run_id == run_id).first()
        update_pipeline_run_summary.status = RUNNING
        session.add(update_pipeline_run_summary)
        # take all the proteomes that are in the run
        all_proteins_of_run = session.query(ProteinResults).filter(ProteinResults.run_id == run_id).all()
        all_proteins_ids = [protein.query_id for protein in all_proteins_of_run]
        all_proteins_data = session.query(Proteomes).filter(Proteomes.id.in_(all_proteins_ids)).all()
        sequence_list = [[protein.id, protein.sequence] for protein in all_proteins_data]

        

    session.commit()
    session.close()


    parallelised_data = spark.sparkContext.parallelize(sequence_list, numSlices=num_workers)
    parallelised_data.foreach(lambda x: process_sequence(x[0], x[1], run_id,  sequence_list.index(x)))

    merge_results_path = f"{ROOT_DIR}/data/output/{run_id}/merge_results.csv"
    profile_path = f"{ROOT_DIR}/data/output/{run_id}/profile.csv"
    best_hits_path = f"{ROOT_DIR}/data/output/{run_id}/best_hits.csv"

    merge_results(run_id, merge_results_path)
    write_best_hits(best_hits_path, run_id)
    avg_score_std = get_avg_score_std(run_id)
    avg_score_gmean = get_avg_score_gmean(run_id)
    write_profile_csv(avg_score_std, avg_score_gmean, profile_path)
    total_time = time.time() - start_time
    save_results_to_db(avg_score_std, avg_score_gmean, total_time, run_id)
    zip_results(run_id, merge_results_path, profile_path, best_hits_path)
    spark.stop()