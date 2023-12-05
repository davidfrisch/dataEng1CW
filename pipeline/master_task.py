import csv
import sys
import os
import boto3
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pipeline.constants import ROOT_DIR
from pipeline.database import create_session
from pipeline.models.protein_results import ProteinResults
from pipeline.models.pipeline_run_summary import PipelineRunSummary
# Define the indices of the columns in the results file
QUERY_ID_INDEX = 0
BEST_HIT_INDEX = 1
BEST_EVALUE_INDEX = 2
BEST_SCORE_INDEX = 3
SCORE_MEAN_INDEX = 4
SCORE_STD_INDEX = 5
SCORE_GMEAN_INDEX = 6

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

    with open(f"{ROOT_DIR}/output/{run_id}/merge_result.csv", "w") as fh_out:
        fh_out.write("query_id,best_hit,best_evalue,best_score,score_mean,score_std,score_gmean\n")
        for line in results:
            if line != "":
                fh_out.write(line + "\n")

    print(f"Results written to {ROOT_DIR}/output/{run_id}/merge_result.csv")



def write_best_hits(merged_results_csv, output_file):
    """
    Function to write the best hits to the output file
    """
    csv_reader = csv.reader(open(merged_results_csv, "r"), delimiter=",")

    # Skip the header row
    header = next(csv_reader)
    # Extract query_id and best_hit indices from the header
    query_id_index = int(header.index('query_id'))
    best_hit_index = int(header.index('best_hit'))

    if not (isinstance(query_id_index, int) and isinstance(best_hit_index, int)):
        print("Cannot find query_id and best_hit columns in the results file")
        raise Exception("Cannot find query_id and best_hit columns in the results file")

    # Iterate over the rows and extract query_id and best_hit values
    best_hits = []
    for row in csv_reader:
        best_hits.append((row[query_id_index], row[best_hit_index]))

    # Write the best hits to the output file
    with open(output_file, "w") as fh_out:
        fh_out.write("fasta_id,best_hit_id\n")
        for best_hit in best_hits:
            fh_out.write(f"{best_hit[0]},{best_hit[1]}\n")


def get_avg_score_std(merged_results_csv):
    """
    Function to get the average score standard deviation
    """
    csv_reader = csv.reader(open(merged_results_csv, "r"), delimiter=",")
    header = next(csv_reader)

    score_std_index = int(header.index('score_std'))

    if not isinstance(score_std_index, int):
        print("Cannot find score_std column in the results file")
        raise Exception("Cannot find score_std column in the results file")
    
    score_std = []
    for row in csv_reader:
        row_std = str(row[score_std_index])
        # check if the value is not NaN
        if row_std.lower() != 'nan':
            score_std.append(float(row_std))  

    if len(score_std) == 0:
        print("No valid values found in the results file")
        raise Exception("No valid values found in the results file")

    avg_score_std = sum(score_std)/len(score_std)
    return avg_score_std


def get_avg_score_gmean(merged_results_csv):
    """
    Function to get the average score geometric mean
    """
    csv_reader = csv.reader(open(merged_results_csv, "r"), delimiter=",")
    header = next(csv_reader)

    score_gmean_index = int(header.index('score_gmean'))

    if not isinstance(score_gmean_index, int):
        print("Cannot find score_gmean column in the results file")
        raise Exception("Cannot find score_gmean column in the results file")
    
    score_gmean = []
    for row in csv_reader:
        row_gmean = str(row[score_gmean_index])
        # check if the value is not NaN
        if row_gmean.lower() != 'nan':
            score_gmean.append(float(row_gmean))  

    if len(score_gmean) == 0:
        print("No valid values found in the results file")
        raise Exception("No valid values found in the results file")

    avg_score_gmean = sum(score_gmean)/len(score_gmean)
    return avg_score_gmean


def write_profile_csv(avg_score_std, avg_score_gmean, output_file):
    """
    Function to write the mean Standard Deviation and mean Geometric means for all the sequences 
    """   
    with open(output_file, "w") as fh_out:
        fh_out.write("score_std,score_gmean\n")
        fh_out.write(f"{avg_score_std},{avg_score_gmean}\n")
    

def save_results_to_db(merged_results_csv, avg_score_std, avg_score_gmean, total_time, run_id):
    """
    Function to save the results to the database
    """
    print("SAVING RESULTS TO DATABASE")
    session = None
    whoami = os.getenv('USER')
    try:
        session = create_session()

        # Create a new pipeline_run_summary object
        pipeline_run_summary = PipelineRunSummary(
            run_id=run_id,
            execution_time=total_time,
            score_std=avg_score_std,
            score_gmean=avg_score_gmean,
            date_created=datetime.now(),
            author=whoami
        )

        session.add(pipeline_run_summary)
        session.commit()


        csv_reader = csv.reader(open(merged_results_csv, "r"), delimiter=",")
        header = next(csv_reader)
        for row in csv_reader:
            # Create a new protein_result object
            for i in range(2, len(row)):
                if row[i] == 'nan':
                    row[i] = None
                else:
                    row[i] = float(row[i])

            protein_result = ProteinResults(
            run_id=run_id,
            query_id=row[QUERY_ID_INDEX],
            best_hit=row[BEST_HIT_INDEX],
            best_evalue=row[BEST_EVALUE_INDEX],
            best_score=row[BEST_SCORE_INDEX],
            score_mean=row[SCORE_MEAN_INDEX],
            score_std=row[SCORE_STD_INDEX],
            score_gmean=row[SCORE_GMEAN_INDEX]
            )
            # Add the object to the session
            session.add(protein_result)
        
        session.commit()
        session.close()
    except Exception as e:
        print("Error while saving results to database: ", e)
        if session:
            session.rollback()
            
        raise Exception("Error while saving results to database")
    print("RESULTS SAVED TO DATABASE")