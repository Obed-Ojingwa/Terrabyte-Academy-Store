export const HomePage = () => {
  return (
    <div className="store-dashboard space-y-8">
      {/* Header */}
      <div className="dashboard-heading flex flex-col items-center justify-between px-4 py-8 sm:flex-row sm:items-start">
        <div className="w-full sm:w-1/2">
          <h1 className="mb-4 text-3xl font-bold text-neutral-900 dark:text-neutral-50">
            Dashboard
          </h1>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-xl">
            Overview of your store's performance and key metrics
          </p>
        </div>
        <div className="w-full sm:w-1/2 flex justify-end mt-6 sm:mt-0">
          <a href="/orders" className="inline-flex items-center px-5 py-3 text-sm font-medium text-center text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-neutral-900">
            View Orders
          </a>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {/* Orders Card */}
        <div className="bg-white rounded-xl border border-neutral-200 shadow-sm dark:bg-neutral-900 dark:border-neutral-800">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="text-sm font-medium text-neutral-500 dark:text-neutral-400">
                Orders
              </div>
              <div className="flex h-8 w-8 items-center justify-center bg-blue-50 text-blue-600 dark:bg-blue-900 dark:text-blue-400 rounded-xl">
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.737 1.707h17.414c.921 0 1.366-.857.737-1.707l-2.293-2.293z" />
                </svg>
              </div>
            </div>
            <div className="text-3xl font-bold text-neutral-900 dark:text-neutral-50">
              124
            </div>
            <div className="mt-2 flex items-center text-sm">
              <span className="text-blue-600 dark:text-blue-400 font-medium">+12%</span>
              <span className="ml-1 text-xs text-neutral-500 dark:text-neutral-400">since last week</span>
            </div>
          </div>
        </div>

        {/* Revenue Card */}
        <div className="bg-white rounded-xl border border-neutral-200 shadow-sm dark:bg-neutral-900 dark:border-neutral-800">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="text-sm font-medium text-neutral-500 dark:text-neutral-400">
                Revenue
              </div>
              <div className="flex h-8 w-8 items-center justify-center bg-blue-50 text-blue-600 dark:bg-blue-900 dark:text-blue-400 rounded-xl">
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2v7h2.41l2.072-2.072a1 1 0 001.416 0l2.072 2.072H22v-2.41a2 2 0 00-2-2h-7.39l-.966-.966a1 1 0 00-1.415 0l-.966.966H12V8z" />
                </svg>
              </div>
            </div>
            <div className="text-3xl font-bold text-neutral-900 dark:text-neutral-50">
              $8,420
            </div>
            <div className="mt-2 flex items-center text-sm">
              <span className="text-blue-600 dark:text-blue-400 font-medium">+8%</span>
              <span className="ml-1 text-xs text-neutral-500 dark:text-neutral-400">since last week</span>
            </div>
          </div>
        </div>

        {/* Customers Card */}
        <div className="bg-white rounded-xl border border-neutral-200 shadow-sm dark:bg-neutral-900 dark:border-neutral-800">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="text-sm font-medium text-neutral-500 dark:text-neutral-400">
                Customers
              </div>
              <div className="flex h-8 w-8 items-center justify-center bg-blue-50 text-blue-600 dark:bg-blue-900 dark:text-blue-400 rounded-xl">
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0012 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 008 0z" />
                </svg>
              </div>
            </div>
            <div className="text-3xl font-bold text-neutral-900 dark:text-neutral-50">
              2,340
            </div>
            <div className="mt-2 flex items-center text-sm">
              <span className="text-blue-600 dark:text-blue-400 font-medium">+5%</span>
              <span className="ml-1 text-xs text-neutral-500 dark:text-neutral-400">since last week</span>
            </div>
          </div>
        </div>

        {/* Inventory Card */}
        <div className="bg-white rounded-xl border border-neutral-200 shadow-sm dark:bg-neutral-900 dark:border-neutral-800">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="text-sm font-medium text-neutral-500 dark:text-neutral-400">
                Inventory Items
              </div>
              <div className="flex h-8 w-8 items-center justify-center bg-blue-50 text-blue-600 dark:bg-blue-900 dark:text-blue-400 rounded-xl">
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m2 0a9 9 0 01-18 0 9 9 0 0018 0z" />
                </svg>
              </div>
            </div>
            <div className="text-3xl font-bold text-neutral-900 dark:text-neutral-50">
              156
            </div>
            <div className="mt-2 flex items-center text-sm">
              <span className="text-blue-600 dark:text-blue-400 font-medium">-3%</span>
              <span className="ml-1 text-xs text-neutral-500 dark:text-neutral-400">since last week</span>
            </div>
          </div>
        </div>
      </div>

      {/* Revenue trend */}
      <section className="revenue-panel rounded-lg border bg-white p-6">
        <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-sm font-medium text-neutral-500">Revenue overview</p>
            <h2 className="mt-1 text-2xl font-bold text-neutral-900">$8,420.00</h2>
          </div>
          <div className="rounded-md bg-emerald-50 px-3 py-1.5 text-sm font-semibold text-emerald-700">
            +8.2% this week
          </div>
        </div>
        <div className="revenue-chart" role="img" aria-label="Revenue trend rising through the week">
          <svg viewBox="0 0 720 190" preserveAspectRatio="none" aria-hidden="true">
            <defs>
              <linearGradient id="revenue-fill" x1="0" x2="0" y1="0" y2="1">
                <stop offset="0%" stopColor="#2f8062" stopOpacity="0.2" />
                <stop offset="100%" stopColor="#2f8062" stopOpacity="0" />
              </linearGradient>
            </defs>
            <path className="chart-area" d="M0 151 C42 140 55 148 90 128 S145 136 180 112 S237 124 270 94 S330 104 360 87 S420 98 450 68 S510 88 540 54 S600 75 630 42 S684 53 720 18 V190 H0 Z" />
            <path className="chart-line" d="M0 151 C42 140 55 148 90 128 S145 136 180 112 S237 124 270 94 S330 104 360 87 S420 98 450 68 S510 88 540 54 S600 75 630 42 S684 53 720 18" />
          </svg>
        </div>
        <div className="mt-3 flex justify-between text-xs font-medium text-neutral-500">
          <span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span>
        </div>
      </section>

      {/* Recent Activity Section */}
      <div className="bg-white rounded-xl border border-neutral-200 shadow-sm dark:bg-neutral-900 dark:border-neutral-800">
        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-neutral-900 dark:text-neutral-50">
              Recent Activity
            </h2>
            <a href="#" className="text-sm text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-200 font-medium">
              View All
            </a>
          </div>
          <div className="space-y-4">
            {/* Activity Item 1 */}
            <div className="flex items-start space-x-3">
              <div className="flex h-5 w-5 items-center justify-center bg-blue-50 text-blue-600 dark:bg-blue-900 dark:text-blue-400 rounded-full shrink-0">
                <svg className="h-2.5 w-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.768 0 3.42 3.42 0 001.946.806 3.42 3.42 0 014.768 0 3.42 3.42 0 001.946.806 3.42 3.42 0 014.768 0 3.42 3.42 0 001.946.806 3.42 3.42 0 001.946.806 3.42 3.42 0 001.946.806 3.42 3.42 0 001.946.806V17a3 3 0 01-3 3H6a3 3 0 01-3-3V4.697z" />
                </svg>
              </div>
              <div className="flex-1 space-y-1">
                <p className="text-sm font-medium text-neutral-900 dark:text-neutral-50">
                  Order #1024 processed successfully
                </p>
                <p className="text-xs text-neutral-500 dark:text-neutral-400">
                  2 minutes ago
                </p>
              </div>
            </div>

            {/* Activity Item 2 */}
            <div className="flex items-start space-x-3">
              <div className="flex h-5 w-5 items-center justify-center bg-blue-50 text-blue-600 dark:bg-blue-900 dark:text-blue-400 rounded-full shrink-0">
                <svg className="h-2.5 w-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M5 13l1.5 1.5L10 11l1.5-1.5L19 7" />
                </svg>
              </div>
              <div className="flex-1 space-y-1">
                <p className="text-sm font-medium text-neutral-900 dark:text-neutral-50">
                  New customer: Jane Smith
                </p>
                <p className="text-xs text-neutral-500 dark:text-neutral-400">
                  15 minutes ago
                </p>
              </div>
            </div>

            {/* Activity Item 3 */}
            <div className="flex items-start space-x-3">
              <div className="flex h-5 w-5 items-center justify-center bg-blue-50 text-blue-600 dark:bg-blue-900 dark:text-blue-400 rounded-full shrink-0">
                <svg className="h-2.5 w-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3" />
                </svg>
              </div>
              <div className="flex-1 space-y-1">
                <p className="text-sm font-medium text-neutral-900 dark:text-neutral-50">
                  Inventory updated: Product X (+5 units)
                </p>
                <p className="text-xs text-neutral-500 dark:text-neutral-400">
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