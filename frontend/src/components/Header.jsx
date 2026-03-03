const Header = ({ apiStatus }) => {
  return (
    <header className="bg-white dark:bg-slate-800 shadow-sm border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4 max-w-5xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            {/* <div className="text-2xl">🎤</div> */}
            <div>
              <h1 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                Audio Transcription
              </h1>
              <p className="text-xs text-gray-500 dark:text-gray-400">HuggingFace AI Models</p>
            </div>
          </div>
          <div className="flex items-center">
            {apiStatus.checking ? (
              <span className="status-badge bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">
                <span className="inline-block w-2 h-2 bg-gray-400 rounded-full mr-2"></span>
                Checking...
              </span>
            ) : apiStatus.online ? (
              <span className="status-badge bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400">
                <span className="inline-block w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                Online
              </span>
            ) : (
              <span className="status-badge bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400">
                <span className="inline-block w-2 h-2 bg-red-500 rounded-full mr-2"></span>
                Offline
              </span>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
