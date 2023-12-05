import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient();

export default {
  insertFastaDataFileInDB: async ({ id, seq }) => {
    try {
      await prisma.proteomes.create({
        data: {
          id: id,
          sequence: seq,
        },
      });
      console.log("Data inserted");
    } catch (error) {
      console.log(error);
    }
  },
};
