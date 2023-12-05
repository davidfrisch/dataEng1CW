import ProteinsService from "../services/proteins.js";
import RunsService from "../services/runs.js";

export const ProteinsController = {
  getProtein: async (req, res) => {
    const id = req.params.id?.trim();
    if (!id) {
      res.status(400).send("No id provided");
    }
    const protein = await ProteinsService.getProtein(id);
    const runs = await RunsService.getRunsByProteinId(id);

    res.send({
      status: protein?.id ? "success" : "NOT_FOUND",
      id: protein?.id || null,
      sequence: protein?.sequence || null,
      runs: runs || [],
    });
  },
};
