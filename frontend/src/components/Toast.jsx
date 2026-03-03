import { useEffect } from 'react';

const Toast = ({ message, type = 'success', onClose }) => {
  useEffect(() => {
    const timer = setTimeout(onClose, 5000);
    return () => clearTimeout(timer);
  }, [onClose]);

  const styles = type === 'success' 
    ? 'bg-green-600 dark:bg-green-700 border-green-500 dark:border-green-600' 
    : 'bg-red-600 dark:bg-red-700 border-red-500 dark:border-red-600';
  
  const icon = type === 'success' ? '✓' : '✕';

  return (
    <div className="fixed bottom-6 right-6 z-50 animate-fade-in">
      <div className={`${styles} border rounded-lg p-4 shadow-lg max-w-md text-white`}>
        <div className="flex items-start">
          <span className="text-lg mr-3 font-bold">{icon}</span>
          <div className="flex-1">
            <p className="text-sm font-medium">{message}</p>
          </div>
          <button 
            onClick={onClose}
            className="hover:opacity-75 ml-3 text-xl font-bold transition-opacity"
          >
            ×
          </button>
        </div>
      </div>
    </div>
  );
};

export default Toast;
