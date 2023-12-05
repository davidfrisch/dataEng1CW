import express from 'express'
import { RunsController } from '../controllers/runs.js'

export const ResultsProteinsRouter = express.Router()

ResultsProteinsRouter.get('/', RunsController.getRuns)

ResultsProteinsRouter.get('/:run_id', RunsController.getRun)

ResultsProteinsRouter.get('/:run_id/download', RunsController.downloadRun)