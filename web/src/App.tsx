import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { SiteLayout } from "./components/SiteLayout";
import CartPage from "./pages/CartPage";
import HomePage from "./pages/HomePage";
import InterviewPage from "./pages/InterviewPage";
import ProductPage from "./pages/ProductPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<SiteLayout />}>
          <Route index element={<HomePage />} />
          <Route path="entrevista" element={<InterviewPage />} />
          <Route path="canasta" element={<CartPage />} />
          <Route path="product/:sku" element={<ProductPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
