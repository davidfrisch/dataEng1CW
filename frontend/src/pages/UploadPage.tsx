import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";
import api from "../api";

type Props = {};
const fileTypes = ["fasta", "fa"];

export default function UploadPage({}: Props) {
  const [file, setFile] = useState<any>(null);
  const handleChange = (file: any) => {
    setFile(file);
  };

  const handleSubmit = (e: any) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file[0]);
    api
      .upload(formData)
      .then((res) => console.log(res))
      .catch((err) => console.log(err));
  };

  return (
    <div>
      <h1>Drop the fasta file like if it is hot !</h1>
      <FileUploader
        multiple={true}
        handleChange={handleChange}
        name="file"
        types={fileTypes}
      />
      <div style={{ display: "flex", alignItems: "center" }}>
        <button onClick={() => setFile(null)} style={{ marginRight: "1rem" }}>
          {" "}
          x{" "}
        </button>
        <p>{file ? `File name: ${file[0]?.name}` : "no files uploaded yet"}</p>
      </div>
      <button disabled={!file} onClick={handleSubmit}>
        Submit
      </button>
    </div>
  );
}
