import { STATUS_UPLOAD } from "../constants.js";
import prisma from "./prisma_client.js";

export default {
  saveProteines: async (proteines) => {
    const proteines_status = [];
    for (const proteine of proteines) {
      const { id, seq } = proteine;
      try {
        await prisma.proteomes.create({
          data: {
            id: id,
            sequence: seq,
          },
        });
        proteines_status.push({ id, status: STATUS_UPLOAD.SUCCESS });
      } catch (error) {
        if (error.code === "P2002") {
          console.log(`Proteine ${id} already exist`);
          proteines_status.push({ id, status: STATUS_UPLOAD.ALREADY_EXIST });
        } else {
          console.log(error);
          proteines_status.push({ id, status: STATUS_UPLOAD.ERROR });
        }
      }
    }
    return proteines_status;
  },
};
