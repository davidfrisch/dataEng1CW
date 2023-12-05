import { PrismaClient } from "@prisma/client";
import flaskClient from "./flask_client.js";

const prisma = new PrismaClient();

export default {
  getRuns: async () => {
    const results = prisma.protein_results.findMany({
      distinct: ["run_id"],
      select: {
        run_id: true,
      },
    });

    return results;
  },

  getProteins: async (run_id) => {
    const results = prisma.protein_results.findMany({
      where: {
        run_id: run_id,
      },
    });

    return results;
  },

  startRun: async (fastaFilePath, processName) => {

    const res = await flaskClient.post("/launch_pipeline", {
      file_path: fastaFilePath,
      name: processName,
    });

    return res.data.run_id;
  },

  getRunSummary: async (run_id) => {
    const results = await prisma.pipeline_run_summary.findUnique({
      where: {
        run_id: run_id,
      },
    });

    return results;
  },

  toCSV: (proteins) => {
    const header = Object.keys(proteins[0]).join(",");
    const rows = proteins.map((row) => Object.values(row).join(","));
    return [header, ...rows].join("\n");
  },
};
