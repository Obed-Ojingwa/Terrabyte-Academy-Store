export const Footer = () => {
  return (
    <footer className="border-t border-gray-100 bg-white dark:bg-gray-900 dark:border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="py-8 text-center text-sm text-gray-500 dark:text-gray-400">
          <span className="block mb-2">© {new Date().getFullYear()} Terrabyte Academy Store. All rights reserved.</span>
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-center space-y-2 sm:space-y-0 sm:space-x-6">
            <a href="#" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
              Terms of Service
            </a>
            <a href="#" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
              Privacy Policy
            </a>
            <a href="#" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
              Contact Us
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};