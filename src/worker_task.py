import sys
from botocore.exceptions import ClientError
from constants import PYTHON3_PATH, HH_SUITE__BIN_PATH, PDB70_PATH, S4PRED_PATH, SRC_DIR
from subprocess import Popen, PIPE
import boto3


def run_s4pred(input_file, out_file):
    """
    Runs the s4pred secondary structure predictor to produce the horiz file
    """
    cmd = [PYTHON3_PATH, S4PRED_PATH + '/run_model.py',
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


def run_hhsearch(a3m_file):
    """
    Run HHSearch to produce the hhr file
    """
    
    cmd = [HH_SUITE__BIN_PATH + '/hhsearch',
           '-i', a3m_file, '-cpu', '1', '-d', 
           PDB70_PATH]
    
    print(f'STEP 3: RUNNING HHSEARCH: {" ".join(cmd)}')
    
    p = Popen(cmd, stdin=PIPE,stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()


def run_parser(hhr_file, output_file):
    """
    Run the worker_results_parser.py over the hhr file to produce the output summary
    """
    cmd = [PYTHON3_PATH, f'{SRC_DIR}/worker_results_parser.py', '-f', hhr_file, '-o', output_file]
    print(f'STEP 4: RUNNING PARSER: {" ".join(cmd)}')
    p = Popen(cmd, stdin=PIPE,stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print(out.decode("utf-8"))


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
