import { Link } from 'react-router-dom';

export const Navbar = () => {
  return (
    <nav className="bg-white border-gray-200 px-2 sm:px-4 py-2.5 shadow-sm dark:bg-gray-800">
      <div className="container mx-auto flex flex-wrap items-center justify-between">
        <div className="flex items-center flex-shrink-0 text-xl font-medium mr-4">
          <Link to="/" className="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-white">
            Terrabyte Admin
          </Link>
        </div>
        <div className="flex items-center flex-1 w-full justify-between sm:justify-start">
          <div className="flex items-center space-x-4">
            <Link to="/orders" className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white dark:focus:ring-offset-gray-800">
              Orders
            </Link>
            <Link to="/payments" className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white dark:focus:ring-offset-gray-800">
              Payments
            </Link>
            <Link to="/shipping" className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white dark:focus:ring-offset-gray-800">
              Shipping
            </Link>
            <Link to="/coupons" className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white dark:focus:ring-offset-gray-800">
              Coupons
            </Link>
            <Link to="/inventory" className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white dark:focus:ring-offset-gray-800">
              Inventory
            </Link>
            <Link to="/wishlist" className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white dark:focus:ring-offset-gray-800">
              Wishlist
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};