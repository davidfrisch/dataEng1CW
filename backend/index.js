import express from "express";
import bodyParser from "body-parser";
import cors from "cors";
import helmet from "helmet";
import "dotenv/config";
import { RunsRouter } from "./routes/runs.js";
import { UploadRouter } from "./routes/upload.js";
import { ProteinsRouter } from "./routes/proteins.js";
import { HealthRouter } from "./routes/health.js";

const app = express();
app.use(cors());
app.use(helmet());
app.use(bodyParser.json({ limit: "100mb" }));

app.get("/", (req, res) => {
  res.send("Hello World!");
});

app.use("/runs", RunsRouter);
app.use("/upload", UploadRouter);
app.use("/proteins", ProteinsRouter);
app.use("/health", HealthRouter);

app.listen(3001, () => {
  console.log("Server is listening on port 3001");
});
