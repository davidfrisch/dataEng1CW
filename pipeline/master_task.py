import sys
import os
from datetime import datetime
import zipfile
from sqlalchemy.sql import functions
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pipeline.constants import ROOT_DIR
from pipeline.database import create_session
from pipeline.models.protein_results import ProteinResults
from pipeline.models.pipeline_run_summary import PipelineRunSummary, SUCCESS
from pipeline.logger import logger

def merge_results(run_id, output_file):
    """
    Function to merge the results from the individual runs
    """
    logger.info("MERGING RESULTS")
    session = None

    try:
        session = create_session()
        protein_results = session.query(ProteinResults).filter(ProteinResults.run_id == run_id).all()

        with open(output_file, "w") as fh_out:
            fh_out.write("query_id,best_hit,best_evalue,best_score,score_mean,score_std,score_gmean\n")
            for protein_result in protein_results:
                fh_out.write(f"{protein_result.query_id},{protein_result.best_hit},{protein_result.best_evalue},{protein_result.best_score},{protein_result.score_mean},{protein_result.score_std},{protein_result.score_gmean}\n")
            
            logger.info(f"Results written to {output_file}")
        
        session.close()
    except Exception as e:
        logger.error("Error while merging results: ", e)
        session.rollback()
        session.close()



def write_best_hits(output_file, run_id):
    """
    Function to write the best hits to the output file
    """

    session = None

    try:
        session = create_session()
        protein_results = session.query(ProteinResults).filter(ProteinResults.run_id == run_id).all()

        with open(output_file, "w") as fh_out:
            fh_out.write("fasta_id,best_hit_id\n")
            for protein_result in protein_results:
                fh_out.write(f"{protein_result.query_id},{protein_result.best_hit}\n")
            
            logger.info(f"Best hits written to {output_file}")
        
        session.close()
    except Exception as e:
        logger.error("Error while writing best hits: ", e)
        session.rollback()
        session.close()


def get_avg_score_std(run_id):
    """
    Function to get the average score standard deviation
    """
    session = None

    try:
        session = create_session()
        # only of run_id
        score_std_sum = session.query(
            functions.sum(ProteinResults.score_std)
        ).filter(ProteinResults.run_id == run_id).scalar()

        score_std_count = session.query(
            functions.count(ProteinResults.score_std)
        ).filter(ProteinResults.run_id == run_id).scalar()

        avg_score_std = score_std_sum/score_std_count
        session.close()
        return avg_score_std

    except Exception as e:
        logger.error("Error while getting average score standard deviation: ", e)
        session.rollback()
        session.close()


def get_avg_score_gmean(run_id):
    """
    Function to get the average score geometric mean
    """

    session = None

    try:
        session = create_session()
        score_gmean_sum = session.query(
            functions.sum(ProteinResults.score_gmean)
        ).filter(ProteinResults.run_id == run_id).scalar()
        score_gmean_count = session.query(
            functions.count(ProteinResults.score_gmean)
        ).filter(ProteinResults.run_id == run_id).scalar()

        avg_score_gmean = score_gmean_sum/score_gmean_count
        session.close()
        return avg_score_gmean

    except Exception as e:
        logger.error("Error while getting average score geometric mean: ", e)
        session.rollback()
        session.close()


def write_profile_csv(avg_score_std, avg_score_gmean, output_file):
    """
    Function to write the mean Standard Deviation and mean Geometric means for all the sequences 
    """   
    with open(output_file, "w") as fh_out:
        fh_out.write("score_std,score_gmean\n")
        fh_out.write(f"{avg_score_std},{avg_score_gmean}\n")
    

def save_results_to_db(avg_score_std, avg_score_gmean, total_time, run_id):
    """
    Function to save the results to the database
    """
    logger.info("SAVING RESULTS TO DATABASE")
    session = None
   
    try:
        session = create_session()

        new_pipeline_run_summary = session.query(PipelineRunSummary).filter(PipelineRunSummary.run_id == run_id).first()
        new_pipeline_run_summary.status = SUCCESS
        new_pipeline_run_summary.date_finished = datetime.now()
        new_pipeline_run_summary.duration = total_time
        new_pipeline_run_summary.score_std = avg_score_std
        new_pipeline_run_summary.score_gmean = avg_score_gmean
        
        session.add(new_pipeline_run_summary)
        session.commit()
    except Exception as e:
        logger.error("Error while updating database: ", e)
        session.rollback()
        
    session.close()
    logger.info("RESULTS SAVED TO DATABASE")

def zip_results(run_id: str, merge_file, profile_file, best_hits_file):
    """
    Function to zip the results
    """
    logger.info("ZIPPING RESULTS")
    zip_file = f"{ROOT_DIR}/data/output/{run_id}/results.zip"
    with zipfile.ZipFile(zip_file, 'w') as zip:
        zip.write(merge_file, os.path.basename(merge_file))
        zip.write(profile_file, os.path.basename(profile_file))
        zip.write(best_hits_file, os.path.basename(best_hits_file))
    logger.info(f"ZIPPED RESULTS TO {zip_file}")
