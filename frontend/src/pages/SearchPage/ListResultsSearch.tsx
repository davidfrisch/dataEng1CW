import './styles.css'
type Props = {
  listResults: string[]
  message: string
  setSearch: (id: string) => void
}

export default function ListResultsSearch({listResults, setSearch, message}: Props) {
  return (
    <div>
      <h1>Search Results</h1>
      <p>{message}</p>
      <ul>
        {listResults.map((result, index) => (
          <li key={index}>
            <button onClick={() => setSearch(result)}>{result}</button>
          </li>
        ))}
      </ul>
    
    </div>
  )
}