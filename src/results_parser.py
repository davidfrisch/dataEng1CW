from Bio import SearchIO
import numpy as np
from scipy.stats import gmean
import sys
import os
best_hit = []
best_score = 0
good_hit_scores  = []
id = ''

if len(sys.argv) != 3:
    print("Usage: python results_parser.py <hhr_file> <output_file>")
    sys.exit(1)

hhr_file = sys.argv[1]
output_file = sys.argv[2]

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

fhOut.write(f"{id},{best_hit[0]},{best_hit[1]},{best_hit[2]},{mean},{std},{g_mean}\n")
fhOut.close()
print(f"Results written to {output_file}")