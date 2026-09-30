export const OrdersList = () => {
  return (
    <div className="space-y-6">
      <div className="flex flex-col items-center justify-between px-4 py-8 sm:flex-row sm:items-start">
        <div className="w-full sm:w-1/2">
          <h1 className="mb-2 text-2xl font-bold text-gray-900 dark:text-white">
            Orders
          </h1>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Manage and track customer orders
          </p>
        </div>
        <div className="w-full sm:w-1/2 flex justify-end mt-6 sm:mt-0 space-x-3">
          <a href="/orders/create" className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800">
            Create Order
          </a>
          <button className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 dark:focus:ring-offset-gray-800">
            Import Orders
          </button>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="bg-white rounded-lg shadow-sm dark:bg-gray-800 border border-gray-100 dark:border-gray-700">
        <div className="p-6">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Status</label>
              <select className="w-full px-3 py-2 rounded-md border border-gray-300 bg-white text-sm shadow-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-gray-700 dark:border-gray-600 dark:text-gray-300 dark:focus:border-indigo-500 dark:focus:ring-indigo-500">
                <option value="all">All Statuses</option>
                <option value="pending">Pending</option>
                <option value="processing">Processing</option>
                <option value="shipped">Shipped</option>
                <option value="delivered">Delivered</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Date Range</label>
              <div className="flex space-x-2">
                <input type="date" className="flex-1 px-3 py-2 rounded-md border border-gray-300 bg-white text-sm shadow-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-gray-700 dark:border-gray-600 dark:text-gray-300 dark:focus:border-indigo-500 dark:focus:ring-indigo-500" />
                <span className="text-xs text-gray-500 dark:text-gray-400">to</span>
                <input type="date" className="flex-1 px-3 py-2 rounded-md border border-gray-300 bg-white text-sm shadow-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-gray-700 dark:border-gray-600 dark:text-gray-300 dark:focus:border-indigo-500 dark:focus:ring-indigo-500" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Customer</label>
              <input type="text" placeholder="Search customers..." className="w-full px-3 py-2 rounded-md border border-gray-300 bg-white text-sm shadow-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-gray-700 dark:border-gray-600 dark:text-gray-300 dark:focus:border-indigo-500 dark:focus:ring-indigo-500" />
            </div>
            <div className="flex items-end">
              <button className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800">
                Apply Filters
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Orders Table */}
      <div className="bg-white rounded-lg shadow-sm dark:bg-gray-800 border border-gray-100 dark:border-gray-700 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">
                  ID
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">
                  Order Number
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">
                  Customer
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">
                  Status
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">
                  Items
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">
                  Total
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">
                  Date
                </th>
                <th scope="col" className="relative px-6 py-3">
                  <span className="sr-only">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y dark:bg-gray-800 dark:divide-gray-700">
              {/* Order Row 1 */}
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  1024
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  #1024
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400 flex items-center space-x-2">
                  <div className="flex h-8 w-8 items-center justify-center bg-indigo-100 text-indigo-600 dark:bg-indigo-900 dark:text-indigo-400 rounded-full">
                    JD
                  </div>
                  <div>
                    John Doe
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-medium text-green-800 bg-green-100 dark:bg-green-900 dark:text-green-200">
                    Processing
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  3 items
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  $129.99
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  Jul 20, 2023
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                  <a href="#" className="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-200">
                    View
                  </a>
                  <button className="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-200">
                    Edit
                  </button>
                </td>
              </tr>

              {/* Order Row 2 */}
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  1023
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  #1023
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400 flex items-center space-x-2">
                  <div className="flex h-8 w-8 items-center justify-center bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-400 rounded-full">
                    JS
                  </div>
                  <div>
                    Jane Smith
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-medium text-green-800 bg-green-100 dark:bg-green-900 dark:text-green-200">
                    Delivered
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  2 items
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  $89.50
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  Jul 19, 2023
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                  <a href="#" className="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-200">
                    View
                  </a>
                  <button className="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-200">
                    Edit
                  </button>
                </td>
              </tr>

              {/* Order Row 3 */}
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  1022
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  #1022
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400 flex items-center space-x-2">
                  <div className="flex h-8 w-8 items-center justify-center bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-400 rounded-full">
                    MB
                  </div>
                  <div>
                    Michael Brown
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-medium text-red-800 bg-red-100 dark:bg-red-900 dark:text-red-200">
                    Cancelled
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  1 item
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  $45.00
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  Jul 18, 2023
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                  <a href="#" className="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-200">
                    View
                  </a>
                  <button className="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-200">
                    Edit
                  </button>
                </td>
              </tr>

              {/* Empty State Placeholder - would be hidden when there's data */}
              {/*
              <tr>
                <td className="px-6 py-12 text-center text-gray-500 dark:text-gray-400" colSpan="8">
                  No orders found matching your filters.
                </td>
              </tr>
              */}
            </tbody>
          </table>
        </div>

        {/* Table Footer with Pagination */}
        <div className="border-t border-gray-200 bg-gray-50 dark:border-gray-700 dark:bg-gray-700">
          <div className="px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center text-sm text-gray-500 dark:text-gray-400">
              Showing 3 of 24 orders
            </div>
            <div className="mt-4 sm:mt-0 flex space-x-2">
              <button disabled className="px-3 py-2 rounded-md border border-gray-300 bg-white text-sm text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-gray-700 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-600">
                Previous
              </button>
              <button className="px-3 py-2 rounded-md border border-gray-300 bg-white text-sm text-gray-700 hover:bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-600">
                1
              </button>
              <button className="px-3 py-2 rounded-md border border-gray-300 bg-indigo-600 text-white text-sm hover:bg-indigo-700 dark:bg-indigo-600 dark:hover:text-white">
                2
              </button>
              <button className="px-3 py-2 rounded-md border border-gray-300 bg-white text-sm text-gray-700 hover:bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-600">
                3
              </button>
              <button className="px-3 py-2 rounded-md border border-gray-300 bg-white text-sm text-gray-700 hover:bg-gray-50 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-600">
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};