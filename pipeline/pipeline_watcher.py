import sys
import os
from time import sleep, time
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pipeline.constants import BUCKET_NAME
import boto3 

def argparser():
    """
    Function to parse the command line arguments
    """
    parser = argparse.ArgumentParser(
        prog='PDB Analyse',
        description='runs the data analysis pipeline to predict protein structure',
        epilog='Example: python pipeline_script_pyspark.py -f <input_file> [options]' )
    
    parser.add_argument('-r', '--run_id', help='Unique run id', required=True)
    parser.add_argument('--bucket', help='S3 bucket name', default=BUCKET_NAME)

    args = parser.parse_args()
    return args


def watch_pipeline(run_id, bucket_name: str):
    """
    Function to watch the pipeline
    """
    symbols = "|/-\\"
    print(f"Watching pipeline with {run_id} in bucket {bucket_name}")
    list_of_files_done = []
    while True:
        sleep(1)
        # add a spinner
        sys.stdout.write(" Waiting for new file \r" + symbols[0])
        sys.stdout.flush()
        symbols = symbols[1:] + symbols[0]
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        for obj in bucket.objects.filter(Prefix=f"{run_id}/"):
            if obj.key not in list_of_files_done:
                print("New file found: ", obj.key)
                list_of_files_done.append(obj.key)
             


if __name__ == "__main__":
    args = argparser()
    run_id = None
    bucket = None
    
    if args.run_id is None:
        print("Run id is required")
        sys.exit(1)
    
    run_id = args.run_id

    watch_pipeline(args.run_id, args.bucket)

