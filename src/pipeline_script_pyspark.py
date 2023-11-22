import os
import sys
from subprocess import Popen, PIPE
from Bio import SeqIO
from pyspark.sql import SparkSession
import boto3
from botocore.exceptions import ClientError
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

"""
usage: python pipeline_script.py INPUT.fasta  
approx 5min per analysis
"""
# Set spark environments
PYTHON3_PATH = '/mnt/data/dataEng1CW/venv/bin/python3'
os.environ['PYSPARK_PYTHON'] = PYTHON3_PATH
os.environ['PYSPARK_DRIVER_PYTHON'] = PYTHON3_PATH

def run_parser(hhr_file, output_file):
    """
    Run the results_parser.py over the hhr file to produce the output summary
    """
    cmd = [PYTHON3_PATH, f'{ROOT_DIR}/results_parser.py', hhr_file, output_file]
    print(f'STEP 4: RUNNING PARSER: {" ".join(cmd)}')
    p = Popen(cmd, stdin=PIPE,stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print(out.decode("utf-8"))

def run_hhsearch(a3m_file):
    """
    Run HHSearch to produce the hhr file
    """
    hh_suite_bin_path = "/mnt/data/programs/hh-suite/bin"
    pdb70_path = "/mnt/data/pdb70/pdb70"
    
    cmd = [hh_suite_bin_path + '/hhsearch',
           '-i', a3m_file, '-cpu', '1', '-d', 
           pdb70_path]
    
    print(f'STEP 3: RUNNING HHSEARCH: {" ".join(cmd)}')
    
    p = Popen(cmd, stdin=PIPE,stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()


def read_horiz(tmp_file, horiz_file, a3m_file):
    """
    Parse horiz file and concatenate the information to a new tmp a3m file
    """
    pred = ''
    conf = ''
    print("STEP 2: REWRITING INPUT FILE TO A3M")
    with open(horiz_file) as fh_in:
        for line in fh_in:
            if line.startswith('Conf: '):
                conf += line[6:].rstrip()
            if line.startswith('Pred: '):
                pred += line[6:].rstrip()
    with open(tmp_file) as fh_in:
        contents = fh_in.read()
    with open(a3m_file, "w") as fh_out:
        fh_out.write(f">ss_pred\n{pred}\n>ss_conf\n{conf}\n")
        fh_out.write(contents)

def run_s4pred(input_file, out_file):
    """
    Runs the s4pred secondary structure predictor to produce the horiz file
    """
    s4pref_folder_path = "/mnt/data/programs/s4pred"
    cmd = [PYTHON3_PATH, s4pref_folder_path + '/run_model.py',
           '-t', 'horiz', '-T', '1', input_file]
    print(f'STEP 1: RUNNING S4PRED: {" ".join(cmd)}')
    p = Popen(cmd, stdin=PIPE,stdout=PIPE, stderr=PIPE)
    try:
      out, err = p.communicate()
      
      if err:
        raise Exception(err)
      
      print(out.decode("utf-8"))
      with open(out_file, "w") as fh_out:
        fh_out.write(out.decode("utf-8"))
    
    except Exception as err:
      print("Error running s4pred")
      print(err)
      sys.exit(1)
      

def add_to_mapping(mapping_file, k, index):
    """
    Function to add the sequence id and the index to a mapping file
    """
    with open(mapping_file, "a") as fh_out:
        fh_out.write(f"{k}\t{index}\n")


def upload_file_to_s3(bucket, file_name, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Create an S3 client
    s3_client = boto3.client('s3')

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print("Error uploading file to S3")
        return False
    return True


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


def cleanup(tmp_file, horiz_file, a3m_file, hhr_file):
    print("CLEANING UP")
    lambda_rm = lambda x: os.remove(x)
    list(map(lambda_rm, [tmp_file, horiz_file, a3m_file, hhr_file]))

def process_sequence(k, v, run_id, bucket, index):
    mapping_file = f"{ROOT_DIR}/tmp/mapping.txt"
    tmp_file = f"{ROOT_DIR}/tmp/{index}.fas"
    horiz_file = f"{ROOT_DIR}/tmp/horiz/{index}.horiz"
    a3m_file = f"{ROOT_DIR}/tmp/a3m/{index}.a3m"
    hhr_file = f"{ROOT_DIR}/tmp/a3m/{index}.hhr"
    object_name = f"{run_id}/{index}.out"
    output_file = f"{ROOT_DIR}/output/{run_id}/{index}.out"
    os.makedirs(os.path.dirname(tmp_file), exist_ok=True)
    os.makedirs(os.path.dirname(horiz_file), exist_ok=True)
    os.makedirs(os.path.dirname(a3m_file), exist_ok=True)

    with open(tmp_file, "w") as fh_out:
        fh_out.write(f">{k}\n")
        fh_out.write(f"{v}\n")

    add_to_mapping(mapping_file, k, index)
    run_s4pred(tmp_file, horiz_file)
    read_horiz(tmp_file, horiz_file, a3m_file)
    run_hhsearch(a3m_file)
    run_parser(hhr_file, output_file)
    upload_file_to_s3(bucket, output_file, object_name)
    #cleanup(tmp_file, horiz_file, a3m_file, hhr_file)



def merge_results(bucket, run_id):
    """
    Function to merge the results from the individual runs
    """
    print("MERGING RESULTS")
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    results = []
    # for all files in the folder run_id in the bucket
    for obj in bucket.objects.filter(Prefix=f"{run_id}/"):
        print("Reading file: ", obj.key)
        body = obj.get()['Body'].read().decode('utf-8')
        lines = body.split("\n")
        results.extend(lines)

    with open(f"{ROOT_DIR}/output/{run_id}.csv", "w") as fh_out:
        fh_out.write("query_id,best_hit,best_evalue,best_score,score_mean,score_std,score_gmean\n")
        for line in results:
            fh_out.write(line + "\n")


if __name__ == "__main__":
    run_id = "run_test"
    bucket = "comp0235-ucabfri"

    if len(sys.argv) > 3:
        print("Usage: python script.py input_file [--local]")
        sys.exit(1)

    # if --master is not specified, it will run locally
    spark = None
    if "--local" in sys.argv:
        spark = SparkSession.builder.appName("pdb_analyse").master("local[*]").getOrCreate()
    else:
        spark = SparkSession.builder.appName("pdb_analyse").master("spark://ip-10-0-13-106.eu-west-2.compute.internal:7077").getOrCreate()
    

    if os.path.exists(f"{ROOT_DIR}/output/{run_id}"):
        os.system(f"rm -rf {ROOT_DIR}/output/{run_id}")

    os.makedirs(f"{ROOT_DIR}/output/{run_id}")

    sequences = read_input(sys.argv[1])

    sequence_list = list(sequences.items())

    parallelised_data = spark.sparkContext.parallelize(sequence_list)

    parallelised_data.foreach(lambda x: process_sequence(x[0], x[1], run_id, bucket, sequence_list.index(x)))

    merge_results(bucket, run_id)

    spark.stop()