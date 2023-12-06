import React, { useEffect } from "react";
import ListOfProteins from "../../components/ListOfProteins";
import api from "../../api";
import { useParams } from "react-router-dom";
import { run_summary } from "../../types/run_summary";
import "./styles.css";
type Props = {};

export default function RunSummaryPage({}: Props) {
  const { runId } = useParams();
  const [runResults, setRunResults] = React.useState([]);
  const [runSummary, setRunSummary] = React.useState<run_summary | null>(null);

  const getRunResults = async (id: string) => {
    try {
      const response = await api.runs.getRun(id);
      console.log(response);
      const json = await response.data;
      const { proteins, run_summary } = json;
      setRunSummary(run_summary);
      setRunResults(proteins);
    } catch (err: any) {
      console.error(err.message);
    }
  };

  useEffect(() => {
    if (!runId) return;

    getRunResults(runId);
  }, [runId]);

  useEffect(() => {
    console.log(runResults);
  }, [runResults]);

  return (
    <div>
      <h1>Run Results</h1>
      {runSummary && (
        <div className="run-summary">
          <h2>Run Summary</h2>

          <div className="run-summary-container">
            <div className="run-summary-item-container">
              <div className="run-summary-title-item">Run ID</div>
              <div className="run-summary-item">{runSummary.run_id}</div>
            </div>

            <div className="run-summary-item-container">
              <div className="run-summary-title-item">Run time</div>
              <div className="run-summary-item">
                {Math.floor(runSummary.execution_time / 60) +
                  "m " +
                  (runSummary.execution_time % 60).toFixed(0) +
                  "s"}
              </div>
            </div>

            <div className="run-summary-item-container">
              <div className="run-summary-title-item">Average score STD</div>
              <div className="run-summary-item">{runSummary.score_std}</div>
            </div>

            <div className="run-summary-item-container">
              <div className="run-summary-title-item">Average score gmean</div>
              <div className="run-summary-item">{runSummary.score_gmean}</div>
            </div>

            <div className="run-summary-item-container">
              <div className="run-summary-title-item">Created at</div>
              <div className="run-summary-item">{runSummary.date_created}</div>
            </div>

            <div className="run-summary-item-container">
              <div className="run-summary-title-item">Created by</div>
              <div className="run-summary-item">{runSummary.author}</div>
            </div>
          </div>
        </div>
      )}
      {runResults.length && <ListOfProteins proteins_result={runResults} />}
    </div>
  );
}
