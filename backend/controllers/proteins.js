import ProteinsService from "../services/proteins.js";
import RunsService from "../services/runs.js";

export const ProteinsController = {
  getProtein: async (req, res) => {
    const id = req.params.id?.trim();
    if (!id) {
      res.status(400).send("No id provided");
      return;
    }

    const searchProtein = await ProteinsService.searchProtein(id);

    if(searchProtein.length == 0) {
      res.status(404).send("No protein found");
      return
    }

    if (searchProtein.length > 1){

      const searchResults = searchProtein.slice(0, 20).map((protein) => protein.id);
      const message = searchProtein.length > 20 ? "Showing first 20 results" : "Showing all results";
      res.status(200).send({
        status: "MULTIPLE_FOUND",
        message: message,
        proteins: searchResults,
        runs: [],
      });
      return  
    }

    const idFound = searchProtein[0].id;

    const protein = await ProteinsService.getProtein(idFound);

    const runs = await RunsService.getRunsByProteinId(idFound);

    res.send({
      status: protein?.id ? "success" : "NOT_FOUND",
      id: protein?.id || null,
      sequence: protein?.sequence || null,
      runs: runs || [],
    });
  },

  getProteins: async (req, res) => {
    const ids = req.body.ids;
    if (!ids) {
      res.status(400).send("No ids provided");
    }
    const proteins = await ProteinsService.getProteins(ids);

    res.send(proteins);
  },
};
