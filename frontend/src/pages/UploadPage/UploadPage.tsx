import { useState } from "react";
import { FileUploader } from "react-drag-drop-files";
import api from "../../api";
import { STATUS_COLORMAP, STATUS_UPLOAD } from "../../constants";
import StartRunForm from "../../components/StartRunForm/StartRunForm";
import "./styles.css";
import Pagniation from "../../components/Pagination/Pagniation";

const fileTypes = ["fasta", "fa"];
const itemsPerPage = 10;

export default function UploadPage() {
  const [file, setFile] = useState<any>(null);
  const [uploadedStatus, setUploadedStatus] = useState<any>(null);
  const [currentPage, setCurrentPage] = useState<number>(1);

  const [loading, setLoading] = useState<boolean>(false);
  const handleChange = (file: any) => {
    setFile(file);
    setUploadedStatus(null);
  };

  const handleSubmit = (e: any) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("name", file.name);
    api
      .upload(formData)
      .then((res) => {
        setUploadedStatus(res.data);
      })
      .catch((err) => console.log(err))
      .finally(() => setLoading(false));
  };

  const handleRemoveFile = () => {
    setFile(null);
    setUploadedStatus(null);
  };

  return (
    <div>
      <h1>Drop the fasta file like if it is hot !</h1>
      <p>Add a fasta file to upload the ids with their sequences.</p>
      <div hidden={file}>
        <FileUploader
          multiple={false}
          handleChange={handleChange}
          name="file"
          types={fileTypes}
        />
      </div>
      <div style={{ display: "flex", alignItems: "center" }}>
        {file && (
          <button onClick={handleRemoveFile} style={{ marginRight: "1rem" }}>
            {" "}
            x{" "}
          </button>
        )}
        <p>{file ? `File name: ${file?.name}` : "no file uploaded yet"}</p>
      </div>
      <button disabled={!file} onClick={handleSubmit} hidden={uploadedStatus}>
        Submit
      </button>

      {loading && <p>Uploading...</p>}

      {uploadedStatus?.protein_status?.length && (
        <div>
          <h2>Uploaded sequences</h2>
          <div
            style={{ display: "flex", alignItems: "center", margin: "1rem" }}
          >
            <h3>Color legends:</h3>
            <div style={{ margin: "0 1rem" }}>
              <span style={{ color: STATUS_COLORMAP[STATUS_UPLOAD.SUCCESS] }}>
                SUCCESS
              </span>
            </div>
            <div style={{ marginRight: "1rem" }}>
              <span
                style={{ color: STATUS_COLORMAP[STATUS_UPLOAD.ALREADY_EXIST] }}
              >
                Already Saved
              </span>
            </div>
            <div style={{ marginRight: "1rem" }}>
              <span style={{ color: STATUS_COLORMAP[STATUS_UPLOAD.ERROR] }}>
                Error
              </span>
            </div>
          </div>
          <Pagniation
            setCurrentPage={setCurrentPage}
            totalLenghth={uploadedStatus.protein_status.length}
            itemsPerPage={itemsPerPage}
          />
          <ul className="list-sequences">
            {uploadedStatus.protein_status
              .slice(
                (currentPage - 1) * itemsPerPage,
                currentPage * itemsPerPage
              )
              .map((seq: any) => (
                <li
                  key={seq.id}
                  style={{ display: "flex", alignItems: "center" }}
                >
                  <div
                    style={{
                      height: "1rem",
                      width: "1rem",
                      backgroundColor: STATUS_COLORMAP[seq.status],
                      marginRight: "1rem",
                    }}
                  ></div>
                  <span>{seq.id}</span>
                </li>
              ))}
          </ul>
        </div>
      )}
      {uploadedStatus?.fasta_file_path && (
        <div>
          <StartRunForm fasta_file_path={uploadedStatus?.fasta_file_path} />
        </div>
      )}
    </div>
  );
}
