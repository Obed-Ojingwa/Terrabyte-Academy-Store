export const ShippingList = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col items-center justify-between px-4 py-8 sm:flex-row sm:items-start">
        <div className="w-full sm:w-1/2">
          <h1 className="mb-2 text-2xl font-bold text-neutral-900 dark:text-neutral-50">
            Shipments
          </h1>
          <p className="text-sm text-neutral-500 dark:text-neutral-400">
            Overview of all shipments
          </p>
        </div>
        <div className="w-full sm:w-1/2 flex justify-end mt-6 sm:mt-0">
          <a href="/shipping/create" className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-neutral-900">
            Create Shipment
          </a>
        </div>
      </div>

      {/* Shipments Table */}
      <div className="bg-white rounded-xl border border-neutral-200 shadow-sm overflow-hidden dark:bg-neutral-900 dark:border-neutral-800">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-neutral-200 dark:divide-neutral-700">
            <thead className="bg-neutral-50 dark:bg-neutral-900">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider dark:text-neutral-400">
                  ID
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider dark:text-neutral-400">
                  Order
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider dark:text-neutral-400">
                  Tracking Number
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider dark:text-neutral-400">
                  Carrier
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider dark:text-neutral-400">
                  Status
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider dark:text-neutral-400">
                  Estimated Delivery
                </th>
                <th scope="col" className="relative px-6 py-3">
                  <span className="sr-only">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y dark:bg-neutral-900 dark:divide-neutral-700">
              {/* Shipment Row 1 */}
              <tr className="hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-900 dark:text-neutral-50">
                  1
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  #1001
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  1Z999AA10123456784
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  UPS
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-medium text-blue-800 bg-blue-100 dark:bg-blue-900 dark:text-blue-200">
                    In Transit
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  2023-07-25
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <a href="#" className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-200">
                    View
                  </a>
                </td>
              </tr>

              {/* Shipment Row 2 */}
              <tr className="hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-900 dark:text-neutral-50">
                  2
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  #1002
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  1Z999AA10123456785
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  FedEx
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-medium text-blue-800 bg-blue-100 dark:bg-blue-900 dark:text-blue-200">
                    Delivered
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  2023-07-26
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <a href="#" className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-200">
                    View
                  </a>
                </td>
              </tr>

              {/* Shipment Row 3 */}
              <tr className="hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-900 dark:text-neutral-50">
                  3
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  #1003
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  1Z999AA10123456786
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  DHL
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-medium text-blue-800 bg-blue-100 dark:bg-blue-900 dark:text-blue-200">
                    Pending Pickup
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500 dark:text-neutral-400">
                  2023-07-27
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <a href="#" className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-200">
                    View
                  </a>
                </td>
              </tr>

              {/* Empty State Placeholder */}
              {/*
              <tr>
                <td className="px-6 py-12 text-center text-neutral-500 dark:text-neutral-400" colSpan="6">
                  No shipments found.
                </td>
              </tr>
              */}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};