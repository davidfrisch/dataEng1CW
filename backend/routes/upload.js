import express from 'express'
import { UploadController } from '../controllers/upload.js'

export const UploadRouter = express.Router()

import multer from "multer";

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });
UploadRouter.post('/', upload.single('file'), UploadController.importFile);
