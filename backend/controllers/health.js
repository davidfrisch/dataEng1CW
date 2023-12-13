import HealthService from "../services/health.js";

export const HealthController = {
  getStatus: async (req, res) => {
    const healthPrisma = await HealthService.getHealthPrisma();
    const healthFlask = await HealthService.getHealthFlask();

    res.status(200).json({
      database: healthPrisma,
      ...healthFlask,
    });
  },
};
