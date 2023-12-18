import express from 'express'
import { RunsController } from '../controllers/runs.js'

export const RunsRouter = express.Router()

RunsRouter.get('/', RunsController.getRuns)

RunsRouter.get('/:run_id', RunsController.getRun)

RunsRouter.post('/:run_id/retry', RunsController.retry)

RunsRouter.get('/:run_id/download', RunsController.downloadRun)

RunsRouter.post('/launch_pipeline', RunsController.startRun)