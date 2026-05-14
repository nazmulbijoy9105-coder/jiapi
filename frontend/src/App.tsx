import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import LegislationPage from "./pages/LegislationPage";
import CaseLawPage from "./pages/CaseLawPage";
import SearchPage from "./pages/SearchPage";
import SectionDetailPage from "./pages/SectionDetailPage";

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/legislations/:era" element={<LegislationPage />} />
        <Route path="/legislations/:era/:id" element={<LegislationPage />} />
        <Route path="/legislations/:era/:id/sections/:section" element={<SectionDetailPage />} />
        <Route path="/case-laws" element={<CaseLawPage />} />
        <Route path="/case-laws/:court" element={<CaseLawPage />} />
        <Route path="/search" element={<SearchPage />} />
      </Routes>
    </Layout>
  );
}

export default App;
