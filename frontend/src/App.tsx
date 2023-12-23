import "./App.css";
import { Routes, Route, BrowserRouter } from "react-router-dom";
import RunsPage from "./pages/RunsPage/RunsPage";
import RunSummaryPage from "./pages/RunSummaryPage/RunSummaryPage";
import NavBar from "./components/NavBar/NavBar";
import UploadPage from "./pages/UploadPage/UploadPage";
import SearchPage from "./pages/SearchPage/SearchPage";
import NewRunPage from "./pages/NewRunPage/NewRunPage";

function App() {
  return (
    <>
      <NavBar />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<RunsPage />} />
          <Route path="/runs/:runId" element={<RunSummaryPage />} />
          <Route path="/new-run" element={<NewRunPage />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/upload" element={<UploadPage />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
