import HealthService from "../services/health.js";
import RunsServices from "../services/runs.js";

export const HealthController = {
  getStatus: async (req, res) => {
    await RunsServices.updateRuns();
    const healthPrisma = await HealthService.getHealthPrisma();
    const healthFlask = await HealthService.getHealthFlask();

    res.status(200).json({
      database: healthPrisma,
      ...healthFlask,
    });
  },
};
