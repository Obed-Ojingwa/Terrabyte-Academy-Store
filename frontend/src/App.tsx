import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { HomePage } from './pages/HomePage';
import { OrdersPage } from './pages/orders/OrdersPage';
import { PaymentsPage } from './pages/payments/PaymentsPage';
import { ShippingPage } from './pages/shipping/ShippingPage';
import { CouponsPage } from './pages/coupons/CouponsPage';
import { InventoryPage } from './pages/inventory/InventoryPage';
import { WishlistPage } from './pages/wishlist/WishlistPage';
import { NotFoundPage } from './pages/NotFoundPage';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50 text-gray-900">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/orders" element={<OrdersPage />} />
            <Route path="/payments" element={<PaymentsPage />} />
            <Route path="/shipping" element={<ShippingPage />} />
            <Route path="/coupons" element={<CouponsPage />} />
            <Route path="/inventory" element={<InventoryPage />} />
            <Route path="/wishlist" element={<WishlistPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;