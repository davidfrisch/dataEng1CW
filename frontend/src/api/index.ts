import axios from "axios";
import { BACKEND_URL } from "../constants";

export const api = axios.create({
  baseURL: BACKEND_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

/* all resquest with runs */
const getRuns = () => api.get("/runs");
const getRun = (id: string) => api.get(`/runs/${id}`);

const runs = {
  getRuns,
  getRun,
};

export default {
  runs,
};
