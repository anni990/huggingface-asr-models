const ModelsList = ({ models, onLoad, onUnload, onDelete }) => {
  if (models.length === 0) {
    return (
      <div className="text-center text-gray-500 dark:text-gray-400 py-8">
        <div className="text-3xl mb-2">📭</div>
        <p className="text-sm">No models registered yet</p>
      </div>
    );
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="space-y-3">
      {models.map((model) => (
        <div 
          key={model.model_id}
          className="bg-gray-50 dark:bg-slate-800/30 p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-blue-400 dark:hover:border-blue-600 transition-colors"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1 min-w-0">
              <div className="flex items-center mb-2 gap-2 flex-wrap">
                <span className="font-semibold text-gray-800 dark:text-gray-100 text-sm break-all">
                  {model.model_id}
                </span>
                {model.is_loaded ? (
                  <span className="px-2 py-0.5 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-xs rounded-full border border-green-300 dark:border-green-700 font-medium">
                    Loaded
                  </span>
                ) : (
                  <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 text-xs rounded-full border border-gray-300 dark:border-gray-700 font-medium">
                    Not Loaded
                  </span>
                )}
              </div>
              <div className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                <div className="flex items-center gap-2">
                  <span>Type:</span>
                  <span className="px-2 py-0.5 bg-gray-50 dark:bg-gray-800/50 text-gray-800 dark:text-gray-200 rounded border border-gray-200 dark:border-gray-700 font-medium">
                    {model.model_type}
                  </span>
                </div>
                <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
                  ✅ Speaker diarization via pyannote (universal)
                </div>
                <div className="mt-2">Added: <span className="text-gray-500 dark:text-gray-400">{formatDate(model.added_at)}</span></div>
                {model.last_used && (
                  <div>Last used: <span className="text-gray-500 dark:text-gray-400">{formatDate(model.last_used)}</span></div>
                )}
              </div>
            </div>
            <div className="flex flex-col gap-2 ml-4 flex-shrink-0">
              {!model.is_loaded ? (
                <button
                  onClick={() => onLoad(model.model_id)}
                  className="btn-primary text-xs px-3 py-1.5"
                >
                  Load
                </button>
              ) : (
                <button
                  onClick={() => onUnload(model.model_id)}
                  className="px-3 py-1.5 bg-yellow-600 hover:bg-yellow-700 text-white rounded-md transition-colors text-xs font-medium"
                >
                  Unload
                </button>
              )}
              <button
                onClick={() => onDelete(model.model_id)}
                className="btn-danger text-xs px-3 py-1.5"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ModelsList;
