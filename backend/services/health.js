import flask_client from "./flask_client.js";
import prisma from "./prisma_client.js";

export default {
  getHealthFlask: async () => {
    try {
      const healthFlask = await flask_client.get("/health");
      return healthFlask.data;
    } catch (error) {
      console.log(error);
      return { flask: false };
    }
  },

  getHealthPrisma: async () => {
    try {
      await prisma.$connect();
      return { status: "ALIVE" };
    } catch (error) {
      return false;
    }
  },
};
