import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient();

export default {
  getProtein: async (id) => {
    const proteins = await prisma.proteomes.findUnique({
      where: {
        id: id,
      },
    });

    return proteins;
  },
};
