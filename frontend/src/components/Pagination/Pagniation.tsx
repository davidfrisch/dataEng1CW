import ReactPaginate from "react-paginate";
import "./styles.css";

type Props = {
  setCurrentPage: React.Dispatch<React.SetStateAction<number>>;
  itemsPerPage: number;
  totalLenghth: number;
};

export default function Pagniation({
  setCurrentPage,
  itemsPerPage,
  totalLenghth,
}: Props) {
  const handlePageClick = (event) => {
    const newOffset = (event.selected + 1) * itemsPerPage;
    console.log(
      `User requested page number ${event.selected}, which is offset ${newOffset}`
    );
    setCurrentPage(event.selected + 1);
  };

  return (
    <ReactPaginate
      className="react-paginate"
      breakLabel="..."
      nextLabel="next >"
      onPageChange={handlePageClick}
      pageRangeDisplayed={5}
      pageCount={Math.ceil(totalLenghth / itemsPerPage)}
      previousLabel="< previous"
      renderOnZeroPageCount={null}
    />
  );
}
