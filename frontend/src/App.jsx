import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import TemplateList from "./pages/TemplateList";
import TemplateForm from "./pages/TemplateForm";
import DealList from "./pages/DealList";
import DealForm from "./pages/DealForm";
import DealView from "./pages/DealView";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <div style={{ padding: "2rem" }}>
        <Routes>
          <Route path="/" element={<Navigate to="/templates" />} />
          <Route path="/templates" element={<TemplateList />} />
          <Route path="/templates/new" element={<TemplateForm />} />
          <Route path="/deals" element={<DealList />} />
          <Route path="/deals/new" element={<DealForm />} />
          <Route path="/deals/:dealId/view" element={<DealView />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}