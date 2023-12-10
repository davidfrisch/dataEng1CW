import React from "react";
import api from "../../api";
import "./styles.css";

type Props = {};

export default function RunsPage({}: Props) {
  const [runResults, setRunResults] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  const getRunResults = async () => {
    try {
      const response = await api.runs.getRuns();
      setRunResults(response.data);
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
    return <div>Loading...</div>;
  }

  return (
    <div className="run-page">
      <div className="start-run-container">

      </div>
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
                  <td>{runResults.date_created.split(".")[0]}</td>
                  <td>{(Math.floor(runResults.execution_time / 60) + "m " + (runResults.execution_time % 60).toFixed(0) + "s")}</td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}