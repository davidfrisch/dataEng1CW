import express from "express";
import { HealthController } from "../controllers/health.js";

export const HealthRouter = express.Router();

HealthRouter.get("/", HealthController.getStatus);
