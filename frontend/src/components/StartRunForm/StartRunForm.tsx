import { useState } from "react";
import api from "../../api";
import { SPARK_URL } from "../../constants";

type Props = {
  fasta_file_path: string;
};

export default function StartRunForm({ fasta_file_path }: Props) {
  const [name, setName] = useState<string>("");
  const [status, setStatus] = useState<any>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    try {
      const res = await api.runs.startRun({
        process_name: name.trim(),
        fasta_file_path: fasta_file_path,
      });
      setStatus(res.data);
    } catch (error: any) {
      console.log(error);
      setErrorMessage(error?.response?.data?.error);
    }
  };

  const handleChange = (e: any) => {
    setName(e.target.value);
    setErrorMessage("");
  }

  if (status)
    return (
      <div>
        <h1>Pipeline in process 🚀 !</h1>
        <button>
          <a href={SPARK_URL + "/"} target="_blank" rel="noreferrer">
            Spark UI
          </a>
        </button>
        <p>
          Pipeline <strong>{status.run_id}</strong> started{" "}
        </p>
      </div>
    );

  return (
    <div>
      <h2>Start a new run (Name without spaces)</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="process_name">Name of the run:</label>
        <input
          type="text"
          id="process_name"
          name="process_name"
          value={name}
          onChange={handleChange}
          style={{ margin: "0 1rem" }}
        />

        <input type="submit" value="Start" disabled={!name.trim()} />
      </form>
      {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
    </div>
  );
}
