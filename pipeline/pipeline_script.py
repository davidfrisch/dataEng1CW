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
from pipeline.worker_task import run_s4pred, read_horiz, run_hhsearch, run_parser, update_sequence_database, update_db_status
from pipeline.master_task import merge_results, write_best_hits, write_profile_csv, save_results_to_db, get_avg_score_gmean, get_avg_score_std
import zipfile
from pipeline.database import create_session
from pipeline.models.protein_results import ProteinResults, PENDING
from pipeline.models.pipeline_run_summary import PipelineRunSummary, SUCCESS, RUNNING


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
    print("READING FASTA FILES")
    sequences = {}
    ids = []
    for record in SeqIO.parse(file, "fasta"):
        sequences[record.id] = record.seq
        ids.append(record.id)
    return(sequences)


def process_sequence(identifier, sequence, run_id, index):
    print(f"PROCESSING SEQUENCE {index} with id {identifier}")
    tmp_file = f"{ROOT_DIR}/tmp/{run_id}/{index}.fas"
    horiz_file = f"{ROOT_DIR}/tmp/{run_id}/horiz/{index}.horiz"
    a3m_file = f"{ROOT_DIR}/tmp/{run_id}/a3m/{index}.a3m"
    hhr_file = f"{ROOT_DIR}/tmp/{run_id}/a3m/{index}.hhr"
    object_name = f"{run_id}/{index}.out"
    output_file = f"{ROOT_DIR}/output/{run_id}/{index}.out"

    # Early exit if the folders are not set up correctly
    if not os.path.exists(HH_SUITE__BIN_PATH):
        print("Folder HH_SUITE__BIN_PATH does not exists: ", HH_SUITE__BIN_PATH)
        sys.exit(1)
    if not os.path.exists(PDB70_PATH+"_cs219.ffdata"):
        print("Folder PDB70_PATH does not exists: ", PDB70_PATH)
        sys.exit(1)
    if not os.path.exists(S4PRED_PATH):
        print("Folder S4PRED_PATH does not exists: ", S4PRED_PATH)
        sys.exit(1)
    
    os.makedirs(os.path.dirname(tmp_file), exist_ok=True)
    os.makedirs(os.path.dirname(horiz_file), exist_ok=True)
    os.makedirs(os.path.dirname(a3m_file), exist_ok=True)  

    with open(tmp_file, "w") as fh_out:
        fh_out.write(f">{identifier}\n")
        fh_out.write(f"{sequence}\n")

    update_db_status(run_id, identifier, RUNNING)
    run_s4pred(tmp_file, horiz_file)
    read_horiz(tmp_file, horiz_file, a3m_file)
    run_hhsearch(a3m_file)
    run_parser(hhr_file, output_file)
    update_sequence_database(output_file, run_id, identifier)
    update_db_status(run_id, identifier, SUCCESS)




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
        print("RUNNING LOCALLY")
        master_url = "local[*]"
    if args.run_id:
        run_id = args.run_id
    if args.num_workers:
        num_workers = args.num_workers

    print('url:'+master_url)
    if not (master_url or args.local):
        print("Please set the spark master with --master or run locally with --local")
        sys.exit(1)
    
    spark = SparkSession.builder.appName(run_id).master(master_url).getOrCreate()
    path_to_pipeline_zip = zip_module()
    spark.sparkContext.addPyFile(path_to_pipeline_zip)
  
    
    os.makedirs(f"{ROOT_DIR}/output/{run_id}", exist_ok=True)
    
    print("SPARK SESSION STARTED on ", master_url)
    print("START RUN ID: ", run_id)
    start_time = time.time()

    sequences = read_input(args.input_file)
    sequence_list = list(sequences.items())
    whoami = os.getenv('USER')
    session = create_session()
    new_pipeline_run_summary = PipelineRunSummary(
        run_id=run_id,
        status=RUNNING,
        date_started=datetime.now(),
        author=whoami
    )
    session.add(new_pipeline_run_summary)
    session.commit()

    for sequence in sequence_list:
        id = sequence[0]
        seq = sequence[1]
        new_protein_results = ProteinResults(
            run_id=run_id,
            query_id=id,
            status=PENDING
        )
        session.add(new_protein_results)

    session.commit()
    parallelised_data = spark.sparkContext.parallelize(sequence_list, numSlices=num_workers)
    parallelised_data.foreach(lambda x: process_sequence(x[0], x[1], run_id,  sequence_list.index(x)))

    merge_results(run_id)
    write_best_hits(f"{ROOT_DIR}/output/{run_id}/best_hits_output.csv", run_id)
    avg_score_std = get_avg_score_std(run_id)
    avg_score_gmean = get_avg_score_gmean(run_id)
    write_profile_csv(avg_score_std, avg_score_gmean,  f"{ROOT_DIR}/output/{run_id}/profile_output.csv")
    total_time = time.time() - start_time
    save_results_to_db(avg_score_std, avg_score_gmean, total_time, run_id)
    spark.stop()