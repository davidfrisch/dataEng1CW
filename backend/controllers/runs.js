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

  downloadRun: async (req, res) => {
    const run_id = req.params.run_id;

    const proteins = await ResultsProteinsService.getProteins(run_id);
    const csv = ResultsProteinsService.toCSV(proteins);
    res.setHeader(`Content-disposition`, `attachment; filename=${run_id}.csv`);
    res.set("Content-Type", "text/csv");
    res.status(200).send(csv);
  },
};
