import { protein_result } from "../types/proteins";
import ProteinResult from "./ProteinResult/ProteinResult";

type Props = {
  proteins_result: protein_result[];
};

export default function ListOfProteins({ proteins_result }: Props) {
  return (
    <div>
      <h1>Proteins</h1>
      {proteins_result.map((protein_result) => (
        
        <ProteinResult
          key={protein_result.query_id}
          proteinResult={protein_result}
        />
      ))}
    </div>
  );
}
