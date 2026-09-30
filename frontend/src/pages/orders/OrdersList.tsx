export const OrdersList = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col items-center justify-between px-4 py-8 sm:flex-row sm:items-start">
        <div className="w-full sm:w-1/2">
          <h1 className="mb-2 text-2xl font-bold text-neutral-900 dark:text-neutral-50">
            Orders
          </h1>
          <p className="text-sm text-neutral-500 dark:text-neutral-400">
            Manage and track customer orders
          </p>
        </div>
        <div className="w-full sm:w-1/2 flex justify-end mt-6 sm:mt-0 space-x-3">
          <a href="/orders/create" className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-neutral-900">
            Create Order
          </a>
          <button className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-neutral-900">
            Import Orders
          </button>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="bg-white rounded-xl border border-neutral-200 shadow-sm dark:bg-neutral-900 dark:border-neutral-800">
        <div className="p-6">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <div>
              <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">Status</label>
              <select className="w-full px-3 py-2 rounded-md border border-neutral-300 bg-white text-sm shadow-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-800 dark:border-neutral-700 dark:text-neutral-300 dark:focus:border-blue-500 dark:focus:ring-blue-500">
                <option value="all">All Statuses</option>
                <option value="pending">Pending</option>
                <option value="processing">Processing</option>
                <option value="shipped">Shipped</option>
                <option value="delivered">Delivered</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">Date Range</label>
              <div className="flex space-x-2">
                <input type="date" className="flex-1 px-3 py-2 rounded-md border border-neutral-300 bg-white text-sm shadow-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-800 dark:border-neutral-700 dark:text-neutral-300 dark:focus:border-blue-500 dark:focus:ring-blue-500" />
                <span className="text-xs text-neutral-500 dark:text-neutral-400">to</span>
                <input type="date" className="flex-1 px-3 py-2 rounded-md border border-neutral-300 bg-white text-sm shadow-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-800 dark:border-neutral-700 dark:text-neutral-300 dark:focus:border-blue-500 dark:focus:ring-blue-500" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">Customer</label>
              <input type="text" placeholder="Search customers..." className="w-full px-3 py-2 rounded-md border border-neutral-300 bg-white text-sm shadow-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-800 dark:border-neutral-700 dark:text-neutral-300 dark:focus:border-blue-500 dark:focus:ring-blue-500" />
            </div>
            <div className="flex items-end">
              <button className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-neutral-900">
                Apply Filters
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Orders Table */}
      <div className="bg-white rounded-xl border border-neutral-200 shadow-sm overflow-hidden dark:bg-neutral-900 dark:border-neutral-800">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-neutral-200 dark:divide-neutral-700">
            <thead className="bg-neutral-50 dark:bg-neutral-900">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider dark:text-neutral-400">
                  ID
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider dark:text-neutral-400">
                  Order Number
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider dark:text-neutral-400">
                  Customer
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider dark:text-neutral-400">
                  Status
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider dark:text-neutral-400">
                  Items
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider dark:text-neutral-400">
                  Total
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider dark:text-neutral-400">
                  Date
                </th>
                <th scope="col" className="relative px-6 py-3">
                  <span className="sr-only">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y dark:bg-neutral-900 dark:divide-neutral-700">
              {/* Order Row 1 */}
              <tr className="hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-900 dark:text-neutral-50">
                  1024
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-neutral-900 dark:text-neutral-50">
                  #1024
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400 flex items-center space-x-2">
                  <div className="flex h-8 w-8 items-center justify-center bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-400 rounded-full">
                    JD
                  </div>
                  <div>
                    John Doe
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-medium text-blue-800 bg-blue-100 dark:bg-blue-900 dark:text-blue-200">
                    Processing
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  3 items
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-neutral-900 dark:text-neutral-50">
                  $129.99
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  Jul 20, 2023
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                  <a href="#" className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-200">
                    View
                  </a>
                  <button className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-200">
                    Edit
                  </button>
                </td>
              </tr>

              {/* Order Row 2 */}
              <tr className="hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-900 dark:text-neutral-50">
                  1023
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-neutral-900 dark:text-neutral-50">
                  #1023
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400 flex items-center space-x-2">
                  <div className="flex h-8 w-8 items-center justify-center bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-400 rounded-full">
                    JS
                  </div>
                  <div>
                    Jane Smith
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-medium text-blue-800 bg-blue-100 dark:bg-blue-900 dark:text-blue-200">
                    Delivered
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  2 items
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-neutral-900 dark:text-neutral-50">
                  $89.50
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  Jul 19, 2023
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                  <a href="#" className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-200">
                    View
                  </a>
                  <button className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-200">
                    Edit
                  </button>
                </td>
              </tr>

              {/* Order Row 3 */}
              <tr className="hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-900 dark:text-neutral-50">
                  1022
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-neutral-900 dark:text-neutral-50">
                  #1022
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400 flex items-center space-x-2">
                  <div className="flex h-8 w-8 items-center justify-center bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-400 rounded-full">
                    MB
                  </div>
                  <div>
                    Michael Brown
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-medium text-blue-800 bg-blue-100 dark:bg-blue-900 dark:text-blue-200">
                    Cancelled
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  1 item
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-neutral-900 dark:text-neutral-50">
                  $45.00
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  Jul 18, 2023
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                  <a href="#" className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-200">
                    View
                  </a>
                  <button className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-200">
                    Edit
                  </button>
                </td>
              </tr>

              {/* Empty State Placeholder - would be hidden when there's data */}
              {/*
              <tr>
                <td className="px-6 py-12 text-center text-neutral-500 dark:text-neutral-400" colSpan="8">
                  No orders found matching your filters.
                </td>
              </tr>
              */}
            </tbody>
          </table>
        </div>

        {/* Table Footer with Pagination */}
        <div className="border-t border-neutral-200 bg-neutral-50 dark:border-neutral-700 dark:bg-neutral-900">
          <div className="px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center text-sm text-neutral-500 dark:text-neutral-400">
              Showing 3 of 24 orders
            </div>
            <div className="mt-4 sm:mt-0 flex space-x-2">
              <button disabled className="px-3 py-2 rounded-md border border-neutral-300 bg-white text-sm text-neutral-500 hover:bg-neutral-100 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-800 dark:border-neutral-700 dark:text-neutral-400 dark:hover:bg-neutral-800">
                Previous
              </button>
              <button className="px-3 py-2 rounded-md border border-neutral-300 bg-white text-sm text-neutral-700 hover:bg-neutral-100 dark:bg-neutral-800 dark:border-neutral-700 dark:text-neutral-300 dark:hover:bg-neutral-800">
                1
              </button>
              <button className="px-3 py-2 rounded-md border border-neutral-300 bg-blue-600 text-white text-sm hover:bg-blue-700 dark:bg-blue-500 dark:hover:text-white">
                2
              </button>
              <button className="px-3 py-2 rounded-md border border-neutral-300 bg-white text-sm text-neutral-700 hover:bg-neutral-100 dark:bg-neutral-800 dark:border-neutral-700 dark:text-neutral-300 dark:hover:bg-neutral-800">
                3
              </button>
              <button className="px-3 py-2 rounded-md border border-neutral-300 bg-white text-sm text-neutral-700 hover:bg-neutral-100 dark:bg-neutral-800 dark:border-neutral-700 dark:text-neutral-300 dark:hover:bg-neutral-800">
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};