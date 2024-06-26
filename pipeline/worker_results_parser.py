from Bio import SearchIO
import numpy as np
from scipy.stats import gmean
import os
import argparse

def run_hhr_parser(hhr_file, output_file):
    """
    Function to parse the hhr file and write the results to a csv file
    """
    best_hit = []
    best_score = 0
    good_hit_scores  = []
    id = ''

    for result in SearchIO.parse(hhr_file, 'hhsuite3-text'):
        id=result.id
        for hit in result.hits:
            if hit.score >= best_score:
                best_score = hit.score
                best_hit = [hit.id, hit.evalue, hit.score]
            if hit.evalue < 1.e-5:
                good_hit_scores.append(hit.score)

    if not os.path.exists(output_file):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

    fhOut = open(output_file, "w")
    mean=format(np.mean(good_hit_scores), ".2f")
    std=format(np.std(good_hit_scores), ".2f")
    g_mean=format(gmean(good_hit_scores), ".2f")

    fhOut.write(f"{id},{best_hit[0]},{best_hit[1]},{best_hit[2]},{mean},{std},{g_mean}")
    fhOut.close()
    print(f"Results written to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='HHR Parser', 
                        description='Parse HHR results and write to csv file',
                        epilog='Example: python results_parser.py <hhr_file> <output_file>' )
    parser.add_argument('-f', '--hhr_file', help='HHR file to parse')
    parser.add_argument('-o', '--output_file', help='Output file to write results to')
    args = parser.parse_args()

    args = parser.parse_args()

    hhr_file = args.hhr_file
    output_file = args.output_file
    print(f"Running parser on {hhr_file}")
    run_hhr_parser(hhr_file, output_file)
