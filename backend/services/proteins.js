import prisma from "./prisma_client.js";

export default {
  getProtein: async (id) => {
    const proteins = await prisma.proteomes.findUnique({
      where: {
        id: id,
      },
    });

    

    return proteins;
  },

  searchProtein: async (id) => {
    const proteins = await prisma.proteomes.findMany({
      where: {
        id: {
          contains: id,
          mode: "insensitive",
        },
      },
      select: {
        id: true,
      },
    });

    return proteins;
  },

  getProteins: async (ids) => {
    const proteins = await prisma.proteomes.findMany({
      where: {
        id: {
          in: ids,
        },
      },
    });


    const results = ids.reduce((acc, id) => {
      if(proteins.find((protein) => protein.id === id)) {
        acc[id] = true;
      } else {
        acc[id] = false;
      }
      return acc;
    }, {});

    return results;
  },
};
