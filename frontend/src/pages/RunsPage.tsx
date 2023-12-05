import React from "react";
import api from "../api";

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
    <div>
      <h1>Run Results</h1>
      <table>
        <thead>
          <tr>
            <th>Run ID</th>
          </tr>
        </thead>
        <tbody>
          {runResults.map((runResults: any) => (
            <tr key={runResults.run_id}>
              <td>
                <a href={`/runs/${runResults.run_id}`}>
                  {runResults.run_id}
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
