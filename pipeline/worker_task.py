import sys
import os
from botocore.exceptions import ClientError
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pipeline.constants import PYTHON3_PATH, HH_SUITE__BIN_PATH, PDB70_PATH, S4PRED_PATH, SRC_DIR
from pipeline.worker_results_parser import run_hhr_parser
from pipeline.database import create_session
from pipeline.models.protein_results import ProteinResults, SUCCESS
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

    print(f'STEP 4: RUNNING PARSER: {hhr_file}')
    run_hhr_parser(hhr_file, output_file)
    print(f"STEP 4: OUTPUT FILE: {output_file}")


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

def update_sequence_database(output_file, run_id, identifier):
    """
    Update the sequence database with the results
    """

    # format query_id,best_hit,best_evalue,best_score,score_mean,score_std,score_gmean
    # only 1 line

    result = {}

    with open(output_file) as fh_in:
        line = fh_in.readline()
        fields = line.split(',')
        result['best_hit'] = fields[1]
        result['best_evalue'] = fields[2]
        result['best_score'] = fields[3]
        result['score_mean'] = fields[4]
        result['score_std'] = fields[5]
        result['score_gmean'] = fields[6]



    session = None
    try:
        session = create_session()
        protein_result = session.query(ProteinResults).filter(ProteinResults.run_id == run_id).filter(ProteinResults.query_id == identifier).first()
        protein_result.best_hit = result['best_hit']
        protein_result.best_evalue = result['best_evalue']
        protein_result.best_score = result['best_score']
        protein_result.score_mean = result['score_mean']
        protein_result.score_std = result['score_std']
        protein_result.score_gmean = result['score_gmean']
        session.add(protein_result)
        session.commit()
        session.close()
    except Exception as e:
        print("Error while updating database: ", e)


def update_db_status(run_id, identifier, status):
    """
    Update the status of the protein in the database
    """
    session = None
    try:
        session = create_session()
        protein_result = session.query(ProteinResults).filter(ProteinResults.run_id == run_id).filter(ProteinResults.query_id == identifier).first()
        protein_result.status = status
        session.add(protein_result)
        session.commit()
        session.close()
        print(f"Updated status of {identifier} to {status}")
    except Exception as e:
        print("Error while updating database: ", e)
