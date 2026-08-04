export const HomePage = () => {
  return (
    <div>
      <h1 className="mb-6 text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div className="bg-white rounded-lg shadow dark:bg-gray-700 p-6">
          <h2 className="mb-4 text-lg font-medium text-gray-900 dark:text-white">Orders</h2>
          <p className="mb-4 text-base text-gray-500 dark:text-gray-400">Manage customer orders</p>
          <a href="/orders" className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            View Orders
          </a>
        </div>
        <div className="bg-white rounded-lg shadow dark:bg-gray-700 p-6">
          <h2 className="mb-4 text-lg font-medium text-gray-900 dark:text-white">Payments</h2>
          <p className="mb-4 text-base text-gray-500 dark:text-gray-400">Process and track payments</p>
          <a href="/payments" className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            View Payments
          </a>
        </div>
        <div className="bg-white rounded-lg shadow dark:bg-gray-700 p-6">
          <h2 className="mb-4 text-lg font-medium text-gray-900 dark:text-white">Inventory</h2>
          <p className="mb-4 text-base text-gray-500 dark:text-gray-400">Manage product stock levels</p>
          <a href="/inventory" className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            View Inventory
          </a>
        </div>
        <div className="bg-white rounded-lg shadow dark:bg-gray-700 p-6">
          <h2 className="mb-4 text-lg font-medium text-gray-900 dark:text-white">Coupons</h2>
          <p className="mb-4 text-base text-gray-500 dark:text-gray-400">Create and manage discounts</p>
          <a href="/coupons" className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            View Coupons
          </a>
        </div>
        <div className="bg-white rounded-lg shadow dark:bg-gray-700 p-6">
          <h2 className="mb-4 text-lg font-medium text-gray-900 dark:text-white">Shipping</h2>
          <p className="mb-4 text-base text-gray-500 dark:text-gray-400">Track shipments and deliveries</p>
          <a href="/shipping" className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            View Shipping
          </a>
        </div>
        <div className="bg-white rounded-lg shadow dark:bg-gray-700 p-6">
          <h2 className="mb-4 text-lg font-medium text-gray-900 dark:text-white">Wishlists</h2>
          <p className="mb-4 text-base text-gray-500 dark:text-gray-400">View customer wishlists</p>
          <a href="/wishlist" className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            View Wishlists
          </a>
        </div>
      </div>
    </div>
  );
};