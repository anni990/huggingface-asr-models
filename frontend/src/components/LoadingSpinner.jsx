const LoadingSpinner = ({ message = 'Loading...', subMessage = '' }) => {
  return (
    <div className="flex items-center justify-center space-x-4 py-8">
      <div className="spinner"></div>
      <div>
        <p className="text-sm font-medium text-gray-700 dark:text-gray-200">
          {message}
        </p>
        {subMessage && (
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{subMessage}</p>
        )}
      </div>
    </div>
  );
};

export default LoadingSpinner;
