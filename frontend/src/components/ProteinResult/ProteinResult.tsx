import { protein_result } from "../../types/proteins";
import "./styles.css";
type Props = {
  proteinResult: protein_result;
};

export default function ProteinResult({ proteinResult }: Props) {
  const {
    best_evalue,
    best_hit,
    status,
    best_score,
    score_gmean,
    score_std,
    query_id,
  } = proteinResult;

  return (
    <div className="proteins-result-container">
      <div className="title-id">
        <div
          className={`status-circle ${
            status === "SUCCESS" ? "success" : status === "RUNNING" ? "running" : "pending"
          }`}
        ></div>
        ID: {query_id}
      </div>
     {status === "SUCCESS" && <div className="protein-container">
        {best_hit && <img
          src={`https://cdn.rcsb.org/images/structures/${best_hit
            .split("_")[0]
            .toLowerCase()}_assembly-1.jpeg`}
          alt={`protein_${best_hit.split("_")[0]}`}
          style={{ width: "8rem", height: "8rem" }}
        />}
        <div className="best-item">
          <h4>Best E-Value</h4>
          <p>{best_evalue}</p>
        </div>

        <div className="best-item">
          <h4>Best Hit</h4>
          <p>{best_hit}</p>
        </div>

        <div className="best-item">
          <h4>Best Score</h4>
          <p>{best_score}</p>
        </div>

        <div className="score-gmean">
          <h4>Score GMean</h4>
          <p>{score_gmean}</p>
        </div>

        <div className="score-std">
          <h4>Score STD</h4>
          <p>{score_std}</p>
        </div>
        <div className="actions">
          {best_hit && <button>
            <a
              href={`https://www.rcsb.org/sequence/${best_hit.split("_")[0]}#${
                best_hit.split("_")[1]
              }`}
              target="_blank"
              rel="noreferrer"
            >
              See in RCSB
            </a>
          </button>}
        </div>
      </div>}
    </div>
  );
}
