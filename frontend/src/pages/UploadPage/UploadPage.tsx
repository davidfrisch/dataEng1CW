import { useState } from "react";
import { FileUploader } from "react-drag-drop-files";
import api from "../../api";
import { STATUS_COLORMAP, STATUS_UPLOAD } from "../../constants";
import StartRunForm from "../../components/StartRunForm/StartRunForm";
import "./styles.css";

type Props = {};
const fileTypes = ["fasta", "fa"];

export default function UploadPage({}: Props) {
  const [file, setFile] = useState<any>(null);
  const [uploadedStatus, setUploadedStatus] = useState<any>(null);
  const handleChange = (file: any) => {
    setFile(file);
    console.log(file)
    setUploadedStatus(null);
  };

  const handleSubmit = (e: any) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);
    formData.append("name", file.name);
    api
      .upload(formData)
      .then((res) => {
        setUploadedStatus(res.data);
        console.log(res.data);
      })
      .catch((err) => console.log(err));
  };

  const handleRemoveFile = () => {
    setFile(null);
    setUploadedStatus(null);
  }

  return (
    <div>
      <h1>Drop the fasta file like if it is hot !</h1>
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
        <p>{file ? `File name: ${file?.name}` : "no files uploaded yet"}</p>
      </div>
      <button disabled={!file} onClick={handleSubmit} hidden={uploadedStatus}>
        Submit
      </button>

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
          <ul className="list-sequences">
            {uploadedStatus.protein_status.map((seq: any) => (
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
      {uploadedStatus?.fasta_file_path && <div>
        <StartRunForm fasta_file_path={uploadedStatus?.fasta_file_path} />
      </div>}
    </div>
  );
}
