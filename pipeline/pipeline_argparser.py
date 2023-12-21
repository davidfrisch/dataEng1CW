
from time import time
import argparse
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pipeline.constants import SPARK_MASTER_URL, NUM_WORKERS_DEFAULT

def argparser():
    """
    Function to parse the command line arguments
    """
    
    run_id = "run_" + str(int(time())) + "_pyspark"
    master_url = SPARK_MASTER_URL

    parser = argparse.ArgumentParser(
        prog='PDB Analyse',
        description='runs the data analysis pipeline to predict protein structure',
        epilog='Example: python pipeline_script_pyspark.py -f <input_file> [options]' )
    
    parser.add_argument('-f', '--input_file', help='Input file to run the pipeline on, must be in fasta format')
    parser.add_argument('-i', '--ids', help='Input file containing a list of PDB ids to run the pipeline on')
    parser.add_argument('--local', help='Run the pipeline locally', action='store_true', default=False)
    parser.add_argument('-m', '--master', help='Spark master url', default=master_url)
    parser.add_argument('--run_id', help='Unique run id', default=run_id)
    parser.add_argument('--num_workers', help='Number of workers', default=NUM_WORKERS_DEFAULT)

    args = parser.parse_args()
    return args
