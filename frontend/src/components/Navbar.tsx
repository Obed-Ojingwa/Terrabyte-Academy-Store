import { Link } from 'react-router-dom';

export const Navbar = () => {
  return (
    <nav className="border-b border-gray-100 bg-white dark:bg-gray-900 dark:border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0">
              <span className="text-xl font-bold text-indigo-600 dark:text-indigo-400">
                Terrabyte Admin
              </span>
            </Link>
          </div>
          <div className="flex items-center space-x-4">
            <Link to="/orders" className="px-3 py-2 rounded-md text-sm font-medium text-gray-500 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-800">
              Orders
            </Link>
            <Link to="/payments" className="px-3 py-2 rounded-md text-sm font-medium text-gray-500 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-800">
              Payments
            </Link>
            <Link to="/shipping" className="px-3 py-2 rounded-md text-sm font-medium text-gray-500 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-800">
              Shipping
            </Link>
            <Link to="/coupons" className="px-3 py-2 rounded-md text-sm font-medium text-gray-500 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-800">
              Coupons
            </Link>
            <Link to="/inventory" className="px-3 py-2 rounded-md text-sm font-medium text-gray-500 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-800">
              Inventory
            </Link>
            <Link to="/wishlist" className="px-3 py-2 rounded-md text-sm font-medium text-gray-500 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-800">
              Wishlist
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};