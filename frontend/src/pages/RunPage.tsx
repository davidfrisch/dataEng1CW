import React, { useEffect } from "react";
import ListOfProteins from "../components/ListOfProteins";
import api from "../api";
import { useParams } from "react-router-dom";
import { run_summary } from "../types/run_summary";

type Props = {};

export default function RunPage({}: Props) {
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
        <div>
          <h2>Run Summary</h2>
          <p>Run ID: {runSummary.run_id}</p>
          {/* show in second with 2 decimal places */}
          <p>Run time: {Math.floor(runSummary.execution_time / 60).toFixed(2)} minutes</p>
          <p>Average score STD (standard deviation): {runSummary.score_std}</p>
          <p>Average score gmean (geometric mean): {runSummary.score_gmean}</p>
          <p>Created at: {runSummary.date_created}</p>
          <p>Created by: {runSummary.author}</p>
        </div>
      )}
      {runResults.length && <ListOfProteins proteins_result={runResults} />}
    </div>
  );
}
