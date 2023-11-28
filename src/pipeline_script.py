#!/usr/bin/env python3
import os
import sys
from constants import HH_SUITE__BIN_PATH, PDB70_PATH, S4PRED_PATH, ROOT_DIR
from Bio import SeqIO
from pyspark.sql import SparkSession
from pipeline_argparser import argparser
from worker_task import run_s4pred, read_horiz, run_hhsearch, run_parser, upload_file_to_s3
from master_task import merge_results, write_best_hits, write_profile_csv

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


def process_sequence(identifier, sequence, run_id, bucket, index):
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

    run_s4pred(tmp_file, horiz_file)
    read_horiz(tmp_file, horiz_file, a3m_file)
    run_hhsearch(a3m_file)
    run_parser(hhr_file, output_file)
    upload_file_to_s3(bucket, output_file, object_name)




if __name__ == "__main__":
    # unique random id for this run time + bucket name
    spark = None
    master_url = None
    bucket = None
    run_id = None
    args = argparser()

    if args.master:
        master_url = args.master
    if args.local:
        print("RUNNING LOCALLY")
        master_url = "local[*]"
    if args.bucket:
        bucket = args.bucket
    if args.run_id:
        run_id = args.run_id

    if not (master_url and args.local):
        print("Please set the spark master with --master or run locally with --local")
        sys.exit(1)
    
    spark = SparkSession.builder.appName("pdb_analyse").master(master_url).getOrCreate()

    if not args.run_id:
        os.makedirs(f"{ROOT_DIR}/output/{run_id}")
    
    print("SPARK SESSION STARTED on ", master_url)
    print("START RUN ID: ", run_id)

    sequences = read_input(args.input_file)
    sequence_list = list(sequences.items())

    parallelised_data = spark.sparkContext.parallelize(sequence_list)
    parallelised_data.foreach(lambda x: process_sequence(x[0], x[1], run_id, bucket, sequence_list.index(x)))

    merge_results(bucket, run_id)
    write_best_hits(f"{ROOT_DIR}/output/{run_id}/merge_result.csv", f"{ROOT_DIR}/output/{run_id}/best_hits_output.csv")
    write_profile_csv(f"{ROOT_DIR}/output/{run_id}/merge_result.csv", f"{ROOT_DIR}/output/{run_id}/profile_output.csv")
    spark.stop()