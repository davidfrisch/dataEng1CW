import { protein_result } from "../types/proteins";
import ProteinResult from "./ProteinResult";

type Props = {
  proteins_result: protein_result[];
};

export default function ListOfProteins({ proteins_result }: Props) {
  return (
    <div>
      <h1>Proteins</h1>
      <table>
        <thead>
        
        </thead>
        <tbody>
          {proteins_result.map((protein_result) => (
            <ProteinResult
              key={protein_result.query_id}
              proteinResult={protein_result}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}
