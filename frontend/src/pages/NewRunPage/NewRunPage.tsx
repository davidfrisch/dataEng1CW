import { useEffect, useState } from "react";
import { FileUploader } from "react-drag-drop-files";
import api from "../../api";
import { SPARK_URL } from "../../constants";
import { Link } from "react-router-dom";
import "./styles.css";
import { SyncLoader } from "react-spinners";
const fileTypes = ["txt"];

export default function NewRunPage() {
  const [file, setFile] = useState<any>(null);
  const [idsStatus, setIdsStatus] = useState<any>(null);
  const [nameOfRun, setNameOfRun] = useState<string>("");
  const [isRunStarted, setIsRunStarted] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleReset = () => {
    setFile(null);
    setIdsStatus(null);
    setIsRunStarted(false);
    setNameOfRun("");
  };

  const handleChange = (file: any) => {
    // each line of the file is an id
    setFile(file);

    const reader = new FileReader();
    reader.onload = async (e) => {
      if (!e.target) return;

      const text = e.target.result;
      if (typeof text !== "string") {
        return;
      }
      const ids = text.split("\n");
      try {
        const isIdInDB = await api.proteins.getProteins(ids);
        setIdsStatus(isIdInDB);
      } catch (error) {
        console.log(error);
      } finally {
        setIsLoading(false);
      }
    };
    reader.readAsText(file);
  };

  const handleStartRun = async () => {
    const ids = idsStatus.foundIds;
    const res = await api.runs.startRun({
      ids,
      process_name: nameOfRun.trim(),
    });
    console.log(res);
    if (res.status === 200) {
      setIsRunStarted(true);
    }
  };

  useEffect(() => {
    if (file) {
      setIsLoading(true);
    }
  }, [file]);

  return (
    <div>
      <h1>New Run</h1>
      <h2> Upload a list of ids (txt) </h2>
      <p> Add a txt file with one id per line </p>
      {!file ? (
        <FileUploader
          multiple={false}
          handleChange={handleChange}
          name="file"
          types={fileTypes}
        />
      ) : (
        <div className="file-info">
          <button onClick={handleReset}>Reset</button>
          <div style={{ margin: "0 10px" }}>File name: {file.name}</div>
          <SyncLoader color={"#36D7B7"} loading={isLoading} size={20} />
        </div>
      )}

      {idsStatus?.foundIds?.length === 0 && (
        <div>
          <h2>No ids found</h2>
          <p>Check the file and try again</p>
        </div>
      )}

      {idsStatus?.foundIds?.length > 0 && !isRunStarted && (
        <div>
          <div>
            <h2>Start a run ? (Name without spaces) </h2>

            {idsStatus?.missingIds.length > 0 && (
              <div>All missing ids will not be included in the run</div>
            )}

            <input
              type="text"
              onChange={(e) => setNameOfRun(e.target.value)}
              value={nameOfRun}
            />
            <button
              disabled={!idsStatus}
              onClick={handleStartRun}
              style={{ marginLeft: "10px" }}
            >
              Start
            </button>
          </div>

          <div className="lists-container">
            {idsStatus?.missingIds.length > 0 && (
              <div>
                <div>
                  <h3>Missing Ids ({idsStatus.missingIds.length})</h3>
                  <button>
                    {" "}
                    <Link to="/upload">Add missing ids to the database</Link>
                  </button>
                </div>
                <div className="list">
                  <ul>
                    {idsStatus.missingIds.map((id: string) => (
                      <li key={id}>{id}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {idsStatus?.foundIds.length > 0 &&
              idsStatus?.missingIds.length > 0 && (
                <div>
                  <h3>Found Ids ({idsStatus.foundIds.length})</h3>
                  <div className="list">
                    <ul>
                      {idsStatus.foundIds.map((id: string) => (
                        <li key={id}>{id}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
          </div>
          {idsStatus?.foundIds.length > 0 &&
            idsStatus?.missingIds.length === 0 && (
              <div>
                <h3>All the ids are found ({idsStatus.foundIds.length})</h3>
                <div className="list">
                  <ul>
                    {idsStatus.foundIds.map((id: string) => (
                      <li key={id}>{id}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
        </div>
      )}

      {isRunStarted && (
        <div>
          <h1>Pipeline in process 🚀 !</h1>
          <button>
            <a href={SPARK_URL + "/"} target="_blank" rel="noreferrer">
              Spark UI
            </a>
          </button>
          <p>
            Pipeline <strong>{nameOfRun}</strong> started{" "}
          </p>
        </div>
      )}
    </div>
  );
}
