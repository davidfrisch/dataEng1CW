import React from "react";
import api from "../../api";
import { Link } from "react-router-dom";
import ListResultsSearch from "./ListResultsSearch";

type Props = {};

export default function SearchPage({}: Props) {
  const [proteinId, setProteinId] = React.useState<string>("");
  const [searchResults, setSearchResults] = React.useState<any>(null);

  const handleSearch = async (id: string) => {
    const res = await api.proteins.getProtein(id);
    const data = await res.data;
    setSearchResults(data);
  };

  const enterPressed = (event: any) => {
    const code = event.keyCode || event.which;
    if (code === 13) {
      handleSearch(proteinId);
    }
  };

  const handleSelectId = (id: string) => {
      setProteinId(id)
      handleSearch(id)
  }

  React.useEffect(() => {
    document.addEventListener("keydown", enterPressed, false);
    return () => {
      document.removeEventListener("keydown", enterPressed, false);
    };
  }, [proteinId]);

  return (
    <div>
      <h1>Search Protein</h1>
      <p>Search for a protein by giving its id</p>
      <input
        type="text"
        placeholder="Protein ID"
        value={proteinId}
        onChange={(e) => setProteinId(e.target.value)}
        size={40}
      />
      <button onClick={() => handleSearch(proteinId)}>Search</button>

      {searchResults?.status && (
        <div>
          {searchResults.status == "NOT_FOUND" && (
            <p>No protein found with id: {proteinId}</p>
          )}

          {searchResults.status == "MULTIPLE_FOUND" &&
            ListResultsSearch({
              listResults: searchResults.proteins,
              message: searchResults?.message || "",
              setSearch: handleSelectId,
            })}

          {searchResults.status == "success" && (
            <div style={{ display: "flex" }}>
              <div style={{ marginRight: "20px" }}>
                <h3>Protein ID: {searchResults.id}</h3>
                <textarea
                  value={searchResults.sequence}
                  readOnly
                  style={{ height: "300px", width: "100%" }}
                />
              </div>
              <div>
                <h3>Found in runs with ids:</h3>
                <ul>
                  {searchResults.runs.map((run: any) => (
                    <li key={run.run_id}>
                      <Link
                        to={`/runs/${run.run_id}`}
                        style={{ marginRight: "10px" }}
                      >
                        {run.run_id}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
