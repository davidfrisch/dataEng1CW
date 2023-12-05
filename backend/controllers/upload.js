import fastaReader from "bionode-fasta";
import fs from "fs";
import UploadService from "../services/upload.js";

export const UploadController = {
  importFile: async (req, res) => {
    // in FormData, the file is stored in req.files.file
    const title = req.body.title;
    // dump file to disc
    const filePathFasta = `tmp.fasta`;
    const fileBuffer = Buffer.from(req.file.buffer);
    const file = fileBuffer.toString();
    const proteines = [];
    fs.writeFileSync(filePathFasta, file);

    fastaReader
      .obj(filePathFasta)
      .on("data", async function (data) {
        const { id, seq } = data;
        proteines.push({ id, seq });
      })
      .on("end", async function () {
        const data = await UploadService.saveProteines(proteines);
        return res.json(data);
      });
  },
};
