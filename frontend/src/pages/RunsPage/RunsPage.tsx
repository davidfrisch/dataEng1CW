import React from "react";
import api from "../../api";
import "./styles.css";
import { GridLoader } from "react-spinners";

const sortRuns = (runs: any) => {
  // order runs by first RUNNING, then FAILED, then SUCCESS
  const orderedRuns = runs.sort((a: any, b: any) => {
    if (a.status === "RUNNING") {
      return -1;
    } else if (b.status === "RUNNING") {
      return 1;
    } else if (a.status === "FAILED") {
      return -1;
    } else if (b.status === "FAILED") {
      return 1;
    } else {
      return 0;
    }
  });

  return orderedRuns;
};

export default function RunsPage() {
  const [runResults, setRunResults] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  const getRunResults = async () => {
    try {
      const response = await api.runs.getRuns();

      // order runs by first RUNNING, then FAILED, then SUCCESS
      const orderedRuns = sortRuns(response.data);

      setRunResults(orderedRuns);
    } catch (err: any) {
      console.error(err.message);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    setLoading(true);
    getRunResults();
  }, []);

  if (loading) {
    return <GridLoader color={"#36D7B7"} loading={loading} size={20} />;
  }

  return (
    <div className="run-page">
      <div className="start-run-container"></div>
      <div className="run-results-container">
        <h1>Run Results</h1>
        <table>
          <thead>
            <tr>
              <th>Run ID</th>
              <th>Author</th>
              <th>Created</th>
              <th>Duration</th>
            </tr>
          </thead>
          <tbody>
            {runResults.length > 0 &&
              runResults.map((runResults: any) => (
                <tr key={runResults.run_id}>
                  <td>
                    <a href={`/runs/${runResults.run_id}`}>
                      {runResults.run_id}
                    </a>
                  </td>
                  <td>{runResults.author}</td>
                  <td>{runResults?.date_started?.split(".")[0]}</td>
                  <td>
                    {runResults.status === "SUCCESS"
                      ? Math.floor(runResults.duration / 60) +
                        "m " +
                        (runResults.duration % 60).toFixed(0) +
                        "s"
                      : runResults.status}
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
