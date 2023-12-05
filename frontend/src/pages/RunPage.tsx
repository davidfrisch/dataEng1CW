import React, { useEffect } from "react";
import ListOfProteins from "../components/ListOfProteins";
import api from "../api";
import { useParams } from "react-router-dom";

type Props = {};

export default function RunPage({}: Props) {
  const { runId } = useParams();
  const [runResults, setRunResults] = React.useState([]);

  const getRunResults = async (id: string) => {
    try {
      const response = await api.runs.getRun(id);
      console.log(response);
      const json = await response.data;
      setRunResults(json);
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
      {runResults.length && <ListOfProteins proteins_result={runResults} />}
    </div>
  );
}
