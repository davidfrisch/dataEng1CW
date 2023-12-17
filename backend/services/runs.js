import fs from "fs";
import flaskClient from "./flask_client.js";
import prisma from "./prisma_client.js";
import HealthService from "./health.js";
import { SHARE_DIR } from "../constants.js";
import admZip from "adm-zip";

export default {
  updateRuns: async () => {
    try {
      const sparkStatus = await HealthService.getHealthFlask();
      const { activeapps } = sparkStatus;
      console.log(sparkStatus);
    } catch (error) {
      console.log(error);
    }
  },

  getRuns: async () => {
    const runs = await prisma.pipeline_run_summary.findMany({
      orderBy: {
        date_started: "desc",
      },
    });
    return runs;
  },

  getProteins: async (run_id) => {
    const results = prisma.protein_results.findMany({
      where: {
        run_id: run_id,
      },
      orderBy: {
        status: "asc",
      },
    });

    return results;
  },

  startRunIds: async (ids, processName) => {
    const res = await flaskClient.post("/launch_pipeline", {
      ids: ids,
      name: processName,
    });

    return res.data.run_id;
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

  toCSVZip: async (proteins, run_id) => {
    const header = Object.keys(proteins[0]).join(",");
    const rows = proteins.map((row) => Object.values(row).join(","));
    const filename = `results_db.csv`;
    const output = `${SHARE_DIR}/output/${run_id}/merge_results_db.zip`
    fs.writeFileSync(
      `${SHARE_DIR}/output/${run_id}/${filename}`,
      [header, ...rows].join("\n")
    );
    const zip = new admZip();
    zip.addLocalFile(`${SHARE_DIR}/output/${run_id}/${filename}`);
    zip.writeZip(output);

    return fs.readFileSync(output);
  },

  getZipFile: async (run_id) => {
    try {
      const file = fs.readFileSync(`${SHARE_DIR}/output/${run_id}/results.zip`);
      return file;
    } catch (e) {
      console.log(e);
      return null;
    }
  },

  getRunsByProteinId: async (protein_id) => {
    const results = await prisma.protein_results.findMany({
      where: {
        query_id: protein_id,
      },
      select: {
        run_id: true,
      },
    });

    return results;
  },
};
