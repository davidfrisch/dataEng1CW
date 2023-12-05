import csv
import sys
import os
import boto3
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pipeline.constants import ROOT_DIR
from pipeline.database import create_session
from pipeline.models.protein_results import ProteinResults
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
        sys.exit(1)

    # Iterate over the rows and extract query_id and best_hit values
    best_hits = []
    for row in csv_reader:
        best_hits.append((row[query_id_index], row[best_hit_index]))

    # Write the best hits to the output file
    with open(output_file, "w") as fh_out:
        fh_out.write("fasta_id,best_hit_id\n")
        for best_hit in best_hits:
            fh_out.write(f"{best_hit[0]},{best_hit[1]}\n")

def write_profile_csv(merged_results_csv, output_file):
    """
    Function to write the mean Standard Deviation and mean Geometric means for all the sequences 
    """
    csv_reader = csv.reader(open(merged_results_csv, "r"), delimiter=",")
    header = next(csv_reader)

    score_std_index = int(header.index('score_std'))
    score_gmean_index = int(header.index('score_gmean'))

    if not (isinstance(score_std_index, int) and isinstance(score_gmean_index, int)):
        print("Cannot find score_std and score_gmean columns in the results file")
        sys.exit(1)
    
    score_std = []
    score_gmean = []
    for row in csv_reader:
        row_std = str(row[score_std_index])
        row_gmean = str(row[score_gmean_index])

        # check if the values are not NaN
        if row_std.lower() != 'nan':
            score_std.append(float(row_std))  
        if row_gmean.lower() != 'nan':
            score_gmean.append(float(row_gmean))

    if len(score_std) == 0 or len(score_gmean) == 0:
        print("No valid values found in the results file")
        sys.exit(1)

    with open(output_file, "w") as fh_out:
        fh_out.write("score_std,score_gmean\n")
        fh_out.write(f"{sum(score_std)/len(score_std)},{sum(score_gmean)/len(score_gmean)}\n")

def save_results_to_db(merged_results_csv, run_id):
    """
    Function to save the results to the database
    """
    print("SAVING RESULTS TO DATABASE")
    session = None
    try:
        session = create_session()
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
            
        sys.exit(1)
    print("RESULTS SAVED TO DATABASE")