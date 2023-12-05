import express from 'express'
import ResultsProteinsService from '../services/runs.js'

export const ResultsProteinsRouter = express.Router()

ResultsProteinsRouter.get('/', async (req, res) => {
  const results = await ResultsProteinsService.getRuns()
  res.json(results)
})

ResultsProteinsRouter.get('/:run_id', async (req, res) => {
  const proteins = await ResultsProteinsService.getProteins(req.params.run_id)
  res.json(proteins)
})

ResultsProteinsRouter.get('/:run_id/download', async (req, res) => {
  const run_id = req.params.run_id

  const proteins = await ResultsProteinsService.getProteins(run_id)
  const csv = ResultsProteinsService.toCSV(proteins)
  res.setHeader(`Content-disposition`, `attachment; filename=${run_id}.csv`)
  res.set('Content-Type', 'text/csv')
  res.status(200).send(csv)
})