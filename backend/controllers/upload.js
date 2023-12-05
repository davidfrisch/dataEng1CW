import fastaReader from "bionode-fasta";
import fs from "fs";
import UploadService from "../services/upload.js";
import { SHARE_DIR } from "../constants.js";

export const UploadController = {
  importFile: async (req, res) => {
    // in FormData, the file is stored in req.files.file
    // in FormData, the name 
    try {
      const name = req.body.name;
      // dump file to disc
      const filePathFasta = `${SHARE_DIR}/${name}_${Date.now()}.fasta`;
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
          const protein_status = await UploadService.saveProteines(proteines);
          return res.json({ protein_status, fasta_file_path: filePathFasta });
        });
    } catch (e) {
      console.log(e);
      return res.status(500).json({ error: e });
    }
  },
};
