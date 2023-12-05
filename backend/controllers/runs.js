import RunsService from '../services/runs.js'

export const RunsController = {

  getRuns: async (req, res) => {
    const runs = await RunsService.getRuns()
    res.send(runs)
  },

  getProteins: async (req, res) => {
    const proteins = await RunsService.getProteins(req.params.run_id)
    res.send(proteins)
  },

}