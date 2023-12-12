
from time import time
import argparse
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pipeline.constants import BUCKET_NAME, SPARK_MASTER_URL, NUM_WORKERS_DEFAULT

def argparser():
    """
    Function to parse the command line arguments
    """
    
    run_id = "run_" + str(int(time())) + "_pyspark"
    bucket = BUCKET_NAME
    master_url = SPARK_MASTER_URL

    parser = argparse.ArgumentParser(
        prog='PDB Analyse',
        description='runs the data analysis pipeline to predict protein structure',
        epilog='Example: python pipeline_script_pyspark.py -f <input_file> [options]' )
    
    parser.add_argument('-f', '--input_file', help='Input file to run the pipeline on, must be in fasta format', required=True)
    parser.add_argument('--local', help='Run the pipeline locally', action='store_true', default=False)
    parser.add_argument('-m', '--master', help='Spark master url', default=master_url)
    parser.add_argument('--bucket', help='S3 bucket name', default=bucket)
    parser.add_argument('--run_id', help='Unique run id', default=run_id)
    parser.add_argument('--num_workers', help='Number of workers', default=NUM_WORKERS_DEFAULT)

    args = parser.parse_args()
    return args
