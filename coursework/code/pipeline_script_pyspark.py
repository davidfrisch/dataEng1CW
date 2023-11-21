import os
import sys
from subprocess import Popen, PIPE
from Bio import SeqIO
from pyspark.sql import SparkSession


"""
usage: python pipeline_script.py INPUT.fasta  
approx 5min per analysis
"""

def run_parser(hhr_file):
    """
    Run the results_parser.py over the hhr file to produce the output summary
    """
    cmd = ['python', './results_parser.py', hhr_file]
    print(f'STEP 4: RUNNING PARSER: {" ".join(cmd)}')
    p = Popen(cmd, stdin=PIPE,stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print(out.decode("utf-8"))

def run_hhsearch(a3m_file):
    """
    Run HHSearch to produce the hhr file
    """
    hh_suite_bin_path = "/mnt/data/hh-suite/bin"
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
    s4pref_folder_path = "/mnt/data/s4pred"
    cmd = ['python3', s4pref_folder_path + '/run_model.py',
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

def process_sequence(k, v, index):
    mapping_file = "/mnt/data/DataEng1/coursework/code/tmp/mapping.txt"
    tmp_file = f"/mnt/data/DataEng1/coursework/code/tmp/tmp/{index}.fas"
    horiz_file = f"/mnt/data/DataEng1/coursework/code/tmp/horiz/{index}.horiz"
    a3m_file = f"/mnt/data/DataEng1/coursework/code/tmp/a3m/{index}.a3m"
    hhr_file = f"/mnt/data/DataEng1/coursework/code/tmp/hhr/{index}.hhr"

    os.makedirs(os.path.dirname(tmp_file), exist_ok=True)
    os.makedirs(os.path.dirname(horiz_file), exist_ok=True)
    os.makedirs(os.path.dirname(a3m_file), exist_ok=True)
    os.makedirs(os.path.dirname(hhr_file), exist_ok=True)

    with open(tmp_file, "w") as fh_out:
        fh_out.write(f">{k}\n")
        fh_out.write(f"{v}\n")

    add_to_mapping(mapping_file, k, index)
    run_s4pred(tmp_file, horiz_file)
    read_horiz(tmp_file, horiz_file, a3m_file)
    run_hhsearch(a3m_file)
    run_parser(hhr_file)
    #cleanup(tmp_file, horiz_file, a3m_file, hhr_file)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file")
        sys.exit(1)

    spark = SparkSession.builder.appName("pdb_analyse").getOrCreate()

    sequences = read_input(sys.argv[1])

    sequence_list = list(sequences.items())

    parallelised_data = spark.sparkContext.parallelize(sequence_list)

    parallelised_data.foreach(lambda x: process_sequence(x[0], x[1], sequence_list.index(x)))

    spark.stop()