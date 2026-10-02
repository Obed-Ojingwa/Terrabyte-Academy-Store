import { Link } from 'react-router-dom';

interface SidebarProps {
  open: boolean;
  onToggleOpen: () => void;
}

export const Sidebar = ({ open, onToggleOpen }: SidebarProps) => {
  return (
    <aside className={`store-sidebar fixed left-0 top-0 h-full w-64 border-r border-neutral-200 dark:bg-neutral-900 dark:border-neutral-800 z-20 transition-transform duration-300 ease-in-out ${open ? 'translate-x-0' : '-translate-x-full'} sm:translate-x-0`}>
      {/* For mobile overlay, we need a backdrop; we'll handle in App */}
      <div className="flex h-16 items-center justify-between px-4 border-b border-neutral-200 dark:border-neutral-800">
        <div className="flex-shrink-0">
          <Link to="/" className="flex items-center space-x-3">
            <span className="h-8 w-8 flex items-center justify-center bg-blue-600 text-white rounded-lg text-xl font-bold">
              T
            </span>
            <span className="hidden sm:block font-bold text-xl text-blue-600 dark:text-blue-400">
              Terrabyte
            </span>
          </Link>
        </div>
        <button
          onClick={onToggleOpen}
          className="p-2 rounded-md text-neutral-500 hover:text-neutral-900 bg-neutral-50 hover:bg-neutral-100 dark:text-neutral-400 dark:hover:text-white dark:bg-neutral-800 dark:hover:bg-neutral-700"
          aria-label="Toggle sidebar"
        >
          {/* Hamburger icon */}
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
      <nav className="mt-4 space-y-1 px-2">
        {/* Navigation links */}
        <Link to="/" className="group flex w-full items-center px-3 py-2 rounded-md text-sm font-medium gap-2 text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-white dark:hover:bg-neutral-800">
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 00-1 1h-3m-6 0a1 1 0 001-1h2a1 1 0 001 1h3a1 1 0 011 1h3a1 1 0 001-1v-4a1 1 0 00-1-1h-3a1 1 0 00-1-1z" />
          </svg>
          <span className="hidden sm:block">Dashboard</span>
        </Link>

        <Link to="/orders" className="group flex w-full items-center px-3 py-2 rounded-md text-sm font-medium gap-2 text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-white dark:hover:bg-neutral-800">
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 012 2h2a2 2 0 002-2v-.096a2 2 0 00-.04-.582A8.985 8.985 0 008 3c-2.485 0-4.512 2.012-4.512 4.5C3.47 9.284 4.096 10.5 5 10.5a2 2 0 010 4H9z" />
          </svg>
          <span className="hidden sm:block">Orders</span>
        </Link>

        <Link to="/payments" className="group flex w-full items-center px-3 py-2 rounded-md text-sm font-medium gap-2 text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-white dark:hover:bg-neutral-800">
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2v7h2.41l2.072-2.072a1 1 0 001.416 0l2.072 2.072H22v-2.41a2 2 0 00-2-2h-7.39l-.966-.966a1 1 0 00-1.415 0l-.966.966H12V8z" />
          </svg>
          <span className="hidden sm:block">Payments</span>
        </Link>

        <Link to="/shipping" className="group flex w-full items-center px-3 py-2 rounded-md text-sm font-medium gap-2 text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-white dark:hover:bg-neutral-800">
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
          <span className="hidden sm:block">Shipping</span>
        </Link>

        <Link to="/coupons" className="group flex w-full items-center px-3 py-2 rounded-md text-sm font-medium gap-2 text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-white dark:hover:bg-neutral-800">
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.956c1.54 0 2.502-1.667 1.732-3.138l-3.138-6.562c-.615-1.288-.186-2.854 1.225-3.31l3.31-.615c1.288-.615 2.854.186 3.31 1.225l6.562 3.138c1.667.77 1.667 2.502 0 4.101l-6.562 3.138c-.615 1.288-1.86 2.004-2.224 1.378z" />
          </svg>
          <span className="hidden sm:block">Coupons</span>
        </Link>

        <Link to="/inventory" className="group flex w-full items-center px-3 py-2 rounded-md text-sm font-medium gap-2 text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-white dark:hover:bg-neutral-800">
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m2 0a9 9 0 01-18 0 9 9 0 0018 0z" />
          </svg>
          <span className="hidden sm:block">Inventory</span>
        </Link>

        <Link to="/wishlist" className="group flex w-full items-center px-3 py-2 rounded-md text-sm font-medium gap-2 text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-white dark:hover:bg-neutral-800">
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 21.354l1.804-3.515a2.117 2.117 0 01.521-1.415l2.288-.872a2.119 2.119 0 012.514 0l2.288.872a2.117 2.117 0 01.521 1.415L12 21.354z" />
          </svg>
          <span className="hidden sm:block">Wishlist</span>
        </Link>
      </nav>

      <div className="mt-auto border-t border-neutral-200 dark:border-neutral-800">
        <div className="flex items-center px-4 py-4">
          {/* User avatar placeholder */}
          <div className="h-8 w-8 flex items-center justify-center bg-blue-600 text-white rounded-full text-md font-bold">
            U
          </div>
          <div className="ml-3 flex-1">
            <p className="text-sm font-medium text-neutral-900 dark:text-neutral-50">
              Admin User
            </p>
            <p className="text-xs text-neutral-500 dark:text-neutral-400">
              admin@terrabyte.academy
            </p>
          </div>
        </div>
        <div className="px-4 py-2">
          <Link to="/" className="block w-full text-left text-xs font-medium text-neutral-500 hover:text-neutral-900 dark:text-neutral-400 dark:hover:text-white">
            Settings
          </Link>
          <Link to="/" className="block w-full text-left text-xs font-medium text-neutral-500 hover:text-neutral-900 mt-1 dark:text-neutral-400 dark:hover:text-white">
            Logout
          </Link>
        </div>
      </div>
    </aside>
  );
};