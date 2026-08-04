export const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 px-2 sm:px-4 py-4 text-sm text-gray-500 dark:bg-gray-800 dark:border-gray-700">
      <div className="container mx-auto flex flex-col items-center">
        <span className="mb-2">© {new Date().getFullYear()} Terrabyte Academy Store. All rights reserved.</span>
      </div>
    </footer>
  );
};