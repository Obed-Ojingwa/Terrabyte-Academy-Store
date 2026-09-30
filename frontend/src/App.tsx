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
import { Sidebar } from './components/Sidebar';
import { useState } from 'react';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <BrowserRouter>
      <div className="relative min-h-screen bg-gray-50 text-gray-900">
        {/* Sidebar */}
        <Sidebar open={sidebarOpen} onToggleOpen={() => setSidebarOpen(!sidebarOpen)} />
        {/* Mobile backdrop */}
        {sidebarOpen && (
          <div className="fixed inset-0 bg-black bg-opacity-50 z-20" onClick={() => setSidebarOpen(false)} />
        )}
        {/* Main content */}
        <main className={`flex-1 min-h-screen overflow-y-auto transition-all duration-300 ${sidebarOpen ? 'ml-0' : 'ml-64'} sm:ml-64`}>
          <div className="flex flex-col h-full">
            {/* Navbar */}
            <Navbar onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} />
            <div className="flex-1 px-4 sm:px-6 lg:px-8 py-8 overflow-y-auto">
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
            </div>
          </div>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;