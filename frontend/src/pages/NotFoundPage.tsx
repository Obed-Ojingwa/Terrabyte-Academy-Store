export const NotFoundPage = () => {
  return (
    <div className="min-h-[calc(100vh-64px)] flex flex-col items-center justify-center px-6 py-12">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">404</h1>
        <p className="text-3xl font-semibold text-gray-600 dark:text-gray-300 mb-6">Page Not Found</p>
        <p className="text-lg text-gray-500 dark:text-gray-400 mb-8">
          Sorry, but the page you were trying to view does not exist.
        </p>
        <a href="/" className="inline-flex items-center px-4 py-2 text-sm font-medium text-center text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          Go Home
        </a>
      </div>
    </div>
  );
};