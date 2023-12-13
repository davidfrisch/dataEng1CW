import express from "express";
import { ProteinsController } from "../controllers/proteins.js";

export const ProteinsRouter = express.Router();

ProteinsRouter.get("/:id", ProteinsController.getProtein);

ProteinsRouter.post("/ids", ProteinsController.getProteins);