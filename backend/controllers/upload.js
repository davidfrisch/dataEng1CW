import fastaReader from "bionode-fasta"
import fs from 'fs'
import UploadService from "../services/upload.js";


export const UploadController = {
  importFile: async (req, res) => {
    // in FormData, the file is stored in req.files.file
    const title = req.body.title;
    // dump file to disc 
    const filePath = `tmp.fasta`;
    const fileBuffer = Buffer.from(req.file.buffer);
    const file = fileBuffer.toString();
    fs.writeFileSync(filePath, file);

    fastaReader.obj(filePath).on('data', async function (data) {
      UploadService.insertFastaDataFileInDB(data);
    })
  },
};
