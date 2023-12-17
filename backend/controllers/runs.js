import RunsService from "../services/runs.js";
import { status } from "@prisma/client";


export const RunsController = {
  getRuns: async (req, res) => {
    const runs = await RunsService.getRuns();
    res.send(runs);
  },

  getRun: async (req, res) => {
    const proteins = await RunsService.getProteins(req.params.run_id);
    const run_summary = await RunsService.getRunSummary(req.params.run_id);
    const progress = proteins.reduce((acc, protein) => {
      acc.total += 1;
      acc[protein.status] += 1;
      return acc;
    }, { total: 0, [status.PENDING]: 0, [status.RUNNING]: 0, [status.SUCCESS]: 0, [status.FAILED]: 0 });

    res.send({ proteins, run_summary, progress });
  },

  startRun: async (req, res) => {
    try {
      const { process_name } = req.body;
      const fasta_file_path = req.body?.fasta_file_path;
      const ids = req.body?.ids;

      if (ids?.length > 0) {
        const run_id = await RunsService.startRunIds(ids, process_name);
        res.send({ run_id });
        return;
      }

      if (!fasta_file_path) {
        res.status(400).send({ error: "No fasta file path provided" });
      }

      const run_id = await RunsService.startRun(fasta_file_path, process_name);
      res.send({ run_id });
    } catch (e) {
      console.log(e);
      res.status(500).send({ error: e });
    }
  },

  downloadRun: async (req, res) => {
    const run_id = req.params.run_id;
    const zipFile = await RunsService.getZipFile(run_id);

    // If zip doesn't exist, return zip only with merged csv
    if (!zipFile) {
      console.log("No zip file, returning csv in zip");
      const proteins = await RunsService.getProteins(run_id);
      const csvZIP = await RunsService.toCSVZip(proteins, run_id);
      res.setHeader(`Content-disposition`, `attachment; filename=${run_id}.zip`);
      res.set("Content-Type", "application/zip");
      res.status(200).send(csvZIP);
      return
    }

    res.setHeader(`Content-disposition`, `attachment; filename=${run_id}.zip`);
    res.set("Content-Type", "application/zip");
    res.status(200).send(zipFile);
  },
};
