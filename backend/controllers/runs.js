import RunsService from "../services/runs.js";

export const RunsController = {
  getRuns: async (req, res) => {
    const runs = await RunsService.getRuns();
    res.send(runs);
  },

  getRun: async (req, res) => {
    const proteins = await RunsService.getProteins(req.params.run_id);
    const run_summary = await RunsService.getRunSummary(req.params.run_id);
    res.send({ proteins, run_summary });
  },

  startRun: async (req, res) => {
    try {
      const { fasta_file_path, process_name } = req.body;
      const run_id = await RunsService.startRun(fasta_file_path, process_name);
      res.send({ run_id });
    } catch (e) {
      console.log(e);
      res.status(500).send({ error: e });
    }
  },

  downloadRun: async (req, res) => {
    const run_id = req.params.run_id;

    const proteins = await RunsService.getProteins(run_id);
    const csv = RunsService.toCSV(proteins);
    res.setHeader(`Content-disposition`, `attachment; filename=${run_id}.csv`);
    res.set("Content-Type", "text/csv");
    res.status(200).send(csv);
  },
};
