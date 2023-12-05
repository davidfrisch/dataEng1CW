import "./App.css";
import { Routes, Route, BrowserRouter } from "react-router-dom";
import RunsPage from "./pages/RunsPage";
import RunPage from "./pages/RunPage";
import NavBar from "./components/NavBar/NavBar";
import UploadPage from "./pages/UploadPage";
import MetricsPage from "./pages/MetricsPage";
import SearchPage from "./pages/SearchPage";

function App() {
  return (
    <>
      <NavBar />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<RunsPage />} />
          <Route path="/runs/:runId" element={<RunPage />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/metrics" element={<MetricsPage />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
