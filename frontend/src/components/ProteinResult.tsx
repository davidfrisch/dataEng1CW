import { protein_result } from "../types/proteins";

type Props = {
  proteinResult: protein_result;
};

export default function ProteinResult({ proteinResult }: Props) {
  const {
    run_id,
    best_evalue,
    best_hit,
    best_score,
    query_id,
    score_gmean,
    score_std,
  } = proteinResult;

  return (
    <div>
      <h3>Run ID: {run_id}</h3>
      <p>Best E-Value: {best_evalue}</p>
      <p>Best Hit: {best_hit}</p>
      <p>Best Score: {best_score}</p>
      <p>Query ID: {query_id}</p>
      <p>Score GMean: {score_gmean}</p>
      <p>Score STD: {score_std}</p>
    </div>
  );
}
