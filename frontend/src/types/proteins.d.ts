export type protein_result = {
  run_id: string;
  query_id: string;
  best_hit: float;
  best_evalue: float;
  best_score: float;
  score_std: float;
  score_gmean: float;
}