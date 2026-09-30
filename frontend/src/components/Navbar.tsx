import { Link } from 'react-router-dom';

export const Navbar = () => {
  return (
    <nav className="border-b border-neutral-200 bg-white dark:bg-neutral-900 dark:border-neutral-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0">
              <span className="text-xl font-bold text-blue-600 dark:text-blue-400">
                Terrabyte Admin
              </span>
            </Link>
          </div>
          <div className="flex items-center space-x-4">
            <Link to="/orders" className="px-3 py-2 rounded-md text-sm font-medium text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-white dark:hover:bg-neutral-800">
              Orders
            </Link>
            <Link to="/payments" className="px-3 py-2 rounded-md text-sm font-medium text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-white dark:hover:bg-neutral-800">
              Payments
            </Link>
            <Link to="/shipping" className="px-3 py-2 rounded-md text-sm font-medium text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-white dark:hover:bg-neutral-800">
              Shipping
            </Link>
            <Link to="/coupons" className="px-3 py-2 rounded-md text-sm font-medium text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-white dark:hover:bg-neutral-800">
              Coupons
            </Link>
            <Link to="/inventory" className="px-3 py-2 rounded-md text-sm font-medium text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-white dark:hover:bg-neutral-800">
              Inventory
            </Link>
            <Link to="/wishlist" className="px-3 py-2 rounded-md text-sm font-medium text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-white dark:hover:bg-neutral-800">
              Wishlist
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};