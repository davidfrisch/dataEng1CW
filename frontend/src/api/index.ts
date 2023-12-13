import axios from "axios";
import { BACKEND_URL } from "../constants";

export const api = axios.create({
  baseURL: BACKEND_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

/* all resquest with runs */
const getRuns = async () => {
  const res = await api.get("/runs");
  return res;
};
const getRun = (id: string) => api.get(`/runs/${id}`);

type StartRunData = {
  process_name: string;
  fasta_file_path: string;
};
const startRun = (data: StartRunData) =>
  api.post("/runs/launch_pipeline", data);

const downloadRun = (id: string) => api.get(`/runs/${id}/download`);

const runs = {
  getRuns,
  getRun,
  startRun,
  downloadRun,
};

const upload = (data: any) =>
  api.post("/upload", data, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

const proteins = {
  getProtein: (id: string) => api.get(`/proteins/${id}`),
};

const health = () => api.get("/health");

export default {
  runs,
  upload,
  proteins,
  health,
};
