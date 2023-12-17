import { useEffect, useState } from "react";
import ListOfProteins from "../../components/ListOfProteins";
import api from "../../api";
import { useParams } from "react-router-dom";
import { run_summary } from "../../types/run_summary";
import "./styles.css";
import Pagniation from "../../components/Pagination/Pagniation";
import Timer from "../../components/Timer/Timer";

const itemsPerPage = 10;
const COLOR_MAP = {
  SUCCESS: "green",
  FAILED: "red",
  PENDING: "gray",
  RUNNING: "yellow",
} as { [key: string]: string };

export default function RunSummaryPage() {
  const { runId } = useParams();
  const [runResults, setRunResults] = useState([]);
  const [runSummary, setRunSummary] = useState<run_summary | null>(null);
  const [currentPage, setCurrentPage] = useState<number>(1);

  const getRunResults = async (id: string) => {
    try {
      const response = await api.runs.getRun(id);
      console.log(response);
      const json = await response.data;
      const { proteins, run_summary, progress } = json;
      setRunSummary({ ...run_summary, progress });
      setRunResults(proteins);
    } catch (err: any) {
      console.error(err.message);
    }
  };

  const downloadRunResults = async () => {
    if (!runId) return;

    try {
      const csvFileRes = await api.runs.downloadRun(runId);
      const { data: blob } = csvFileRes;
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      const filename = `results_${runId}.zip`;
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
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
          <div className="run-summary-header">
            <h2>Run Summary</h2>
            {runSummary.status === "RUNNING" && (
              <Timer startDateTime={runSummary.date_started} />
            )}
            {runSummary.status === "FAILED" ||
            runSummary.status === "SUCCESS" && (
              <div className="run-rummary-total-time">
                {Math.floor(runSummary.duration / 60) +
                  "m " +
                  (runSummary.duration % 60).toFixed(0) +
                  "s"}
              </div>
            )}
            <button
              hidden={runSummary.status !== "SUCCESS"}
              onClick={downloadRunResults}
              className="btn btn-primary"
            >
              Download
            </button>
          </div>
          <div>
            {runSummary.progress && (
              <div className="run-summary-progress-container">
                {Object.entries(runSummary.progress).map(([name, value]) => (
                  <div key={name} className="run-summary-progress-item">
                    <div
                      className="run-summary-progress-item-title"
                      style={{ color: COLOR_MAP[name] }}
                    >
                      {name.toUpperCase()}
                    </div>
                    <div className="run-summary-progress-item-value">
                      {value}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="run-summary-container">
            <div className="run-summary-item-container">
              <div className="run-summary-title-item">Run ID</div>
              <div className="run-summary-item">{runSummary.run_id}</div>
            </div>

            <div className="run-summary-item-container">
              <div className="run-summary-title-item">Run time</div>
              <div className="run-summary-item">
                {runSummary.status === "SUCCESS"
                  ? Math.floor(runSummary.duration / 60) +
                    "m " +
                    (runSummary.duration % 60).toFixed(0) +
                    "s"
                  : runSummary.status}
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
              <div className="run-summary-item">
                {runSummary?.date_started?.split(".")[0]}
              </div>
            </div>

            <div className="run-summary-item-container">
              <div className="run-summary-title-item">Created by</div>
              <div className="run-summary-item">{runSummary.author}</div>
            </div>
          </div>
        </div>
      )}
      <Pagniation
        setCurrentPage={setCurrentPage}
        totalLenghth={runResults.length}
        itemsPerPage={itemsPerPage}
      />
      {runResults.length && (
        <ListOfProteins
          proteins_result={runResults.slice(
            (currentPage - 1) * itemsPerPage,
            currentPage * itemsPerPage
          )}
        />
      )}
    </div>
  );
}
