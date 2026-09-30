export const HomePage = () => {
  return (
    <div className="space-y-8">
      <div className="flex flex-col items-center justify-between px-4 py-8 sm:flex-row sm:items-start">
        <div className="w-full sm:w-1/2">
          <h1 className="mb-4 text-3xl font-bold text-gray-900 dark:text-white">
            Dashboard
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-xl">
            Overview of your store's performance and key metrics
          </p>
        </div>
        <div className="w-full sm:w-1/2 flex justify-end mt-6 sm:mt-0">
          <a href="/orders/create" className="inline-flex items-center px-5 py-3 text-sm font-medium text-center text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800">
            Create New Order
          </a>
        </div>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {/* Orders Card */}
        <div className="bg-white rounded-lg shadow-sm dark:bg-gray-800 border border-gray-100 dark:border-gray-700">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="text-sm font-medium text-gray-500 dark:text-gray-400">
                Orders
              </div>
              <div className="flex h-8 w-8 items-center justify-center bg-indigo-100 text-indigo-600 dark:bg-indigo-900 dark:text-indigo-400 rounded-lg">
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.737 1.707h17.414c.921 0 1.366-.857.737-1.707l-2.293-2.293z" />
                </svg>
              </div>
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">
              124
            </div>
            <div className="mt-2 flex items-center text-sm">
              <span className="text-indigo-600 dark:text-indigo-400 font-medium">+12%</span>
              <span className="ml-1 text-xs text-gray-500 dark:text-gray-400">since last week</span>
            </div>
          </div>
        </div>

        {/* Revenue Card */}
        <div className="bg-white rounded-lg shadow-sm dark:bg-gray-800 border border-gray-100 dark:border-gray-700">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="text-sm font-medium text-gray-500 dark:text-gray-400">
                Revenue
              </div>
              <div className="flex h-8 w-8 items-center justify-center bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-400 rounded-lg">
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2v7h2.41l2.072-2.072a1 1 0 011.416 0l2.072 2.072H22v-2.41a2 2 0 00-2-2h-7.39l-.966-.966a1 1 0 00-1.415 0l-.966.966H12V8z" />
                </svg>
              </div>
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">
              $8,420
            </div>
            <div className="mt-2 flex items-center text-sm">
              <span className="text-green-600 dark:text-green-400 font-medium">+8%</span>
              <span className="ml-1 text-xs text-gray-500 dark:text-gray-400">since last week</span>
            </div>
          </div>
        </div>

        {/* Customers Card */}
        <div className="bg-white rounded-lg shadow-sm dark:bg-gray-800 border border-gray-100 dark:border-gray-700">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="text-sm font-medium text-gray-500 dark:text-gray-400">
                Customers
              </div>
              <div className="flex h-8 w-8 items-center justify-center bg-purple-100 text-purple-600 dark:bg-purple-900 dark:text-purple-400 rounded-lg">
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 008 0z" />
                </svg>
              </div>
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">
              2,340
            </div>
            <div className="mt-2 flex items-center text-sm">
              <span className="text-purple-600 dark:text-purple-400 font-medium">+5%</span>
              <span className="ml-1 text-xs text-gray-500 dark:text-gray-400">since last week</span>
            </div>
          </div>
        </div>

        {/* Inventory Card */}
        <div className="bg-white rounded-lg shadow-sm dark:bg-gray-800 border border-gray-100 dark:border-gray-700">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="text-sm font-medium text-gray-500 dark:text-gray-400">
                Inventory Items
              </div>
              <div className="flex h-8 w-8 items-center justify-center bg-yellow-100 text-yellow-600 dark:bg-yellow-900 dark:text-yellow-400 rounded-lg">
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m2 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">
              156
            </div>
            <div className="mt-2 flex items-center text-sm">
              <span className="text-yellow-600 dark:text-yellow-400 font-medium">-3%</span>
              <span className="ml-1 text-xs text-gray-500 dark:text-gray-400">since last week</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity Section */}
      <div className="bg-white rounded-lg shadow-sm dark:bg-gray-800 border border-gray-100 dark:border-gray-700">
        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Recent Activity
            </h2>
            <a href="#" className="text-sm text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-200 font-medium">
              View All
            </a>
          </div>
          <div className="space-y-4">
            {/* Activity Item 1 */}
            <div className="flex items-start space-x-4">
              <div className="flex h-8 w-8 items-center justify-center bg-indigo-100 text-indigo-600 dark:bg-indigo-900 dark:text-indigo-400 rounded-full shrink-0">
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.768 0 3.42 3.42 0 001.946.806 3.42 3.42 0 014.768 0 3.42 3.42 0 001.946.806 3.42 3.42 0 014.768 0 3.42 3.42 0 001.946.806 3.42 3.42 0 014.768 0V17a3 3 0 01-3 3H6a3 3 0 01-3-3V4.697z" />
                </svg>
              </div>
              <div className="flex-1 space-y-1">
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  Order #1024 processed successfully
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  2 minutes ago
                </p>
              </div>
            </div>

            {/* Activity Item 2 */}
            <div className="flex items-start space-x-4">
              <div className="flex h-8 w-8 items-center justify-center bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-400 rounded-full shrink-0">
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M5 13l1.5 1.5L10 11l1.5-1.5L19 7" />
                </svg>
              </div>
              <div className="flex-1 space-y-1">
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  New customer: Jane Smith
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  15 minutes ago
                </p>
              </div>
            </div>

            {/* Activity Item 3 */}
            <div className="flex items-start space-x-4">
              <div className="flex h-8 w-8 items-center justify-center bg-yellow-100 text-yellow-600 dark:bg-yellow-900 dark:text-yellow-400 rounded-full shrink-0">
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3" />
                </svg>
              </div>
              <div className="flex-1 space-y-1">
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  Inventory updated: Product X (+5 units)
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  1 hour ago
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};