import { useEffect, useState } from "react";
import { SPARK_URL } from "../../constants";
import "./styles.css";
import api from "../../api";
type Props = {};

export default function NavBar({}: Props) {
  const [statusServices, setStatusServices] = useState<any>(null);

  function goToRuns() {
    window.location.href = "/";
  }

  function goToUpload() {
    window.location.href = "/upload";
  }

  function goToMetrics() {
    window.open(SPARK_URL+"/", "_blank");
  }

  function goToSearch() {
    window.location.href = "/search";
  }

  function goToNewRun() {
    window.location.href = "/new-run";
  }

  // Update status every 10 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      api
        .health()
        .then((res) => {
          setStatusServices(res.data);
        })
        .catch((err) => console.log(err));
    }, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="navbar-container">
      <div className="navbar-menu">
        <button className="nav-button" onClick={goToUpload}>
          Upload
        </button>
        <button className="nav-button" onClick={goToSearch}>
          Search
        </button>
        <button className="nav-button" onClick={goToNewRun}>
          New Run
        </button>
        <button className="nav-button" onClick={goToRuns}>
          Runs
        </button>
        <button className="nav-button" onClick={goToMetrics}>
          Spark UI
        </button>
      </div>
      <div className="navbar-status">
        {statusServices &&
          Object.keys(statusServices).length > 0 &&
          Object.keys(statusServices).map((key) => {
            return (
              <div className="navbar-status-item" key={key}>
                <div className="navbar-status-item-name">{key}</div>
                <div
                  className={`navbar-status-item-status ${
                    statusServices[key].status?.toLowerCase() === "alive"
                      ? "alive"
                      : "dead"
                  }`}
                >
                  {statusServices[key].status || "OFFLINE"}
                </div>
              </div>
            );
          })}
        <div className="navbar-status-item">
          <div className="navbar-status-item-name">Workers</div>
          <div className="navbar-status-item-status">{statusServices?.spark?.aliveworkers}</div>
        </div>
      </div>
    </div>
  );
}
