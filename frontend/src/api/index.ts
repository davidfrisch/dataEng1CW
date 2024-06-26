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
  ids?: string[];
  fasta_file_path?: string;
};
const startRun = (data: StartRunData) =>
  api.post("/runs/launch_pipeline", data);

const retryRun = (id: string) => api.post(`/runs/${id}/retry`);

const downloadRun = (id: string) => api.get(`/runs/${id}/download`, { responseType: 'blob' });

const runs = {
  getRuns,
  getRun,
  startRun,
  retryRun,
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
  getProteins: async (ids: string[]) => {
    const res = await api.post("/proteins/ids", { ids });
    const proteins = res.data;
    const missingIds = Object.keys(proteins).reduce((acc, id) => {
      if (!proteins[id]) acc.push(id);
      return acc;
    }, [] as string[]);
    const foundIds = Object.keys(proteins).reduce((acc, id) => {
      if (proteins[id]) acc.push(id);
      return acc;
    }, [] as string[]);
    return { missingIds, foundIds };
  },

};



const health = () => api.get("/health");

export default {
  runs,
  upload,
  proteins,
  health,
};
