import { useState, useEffect } from 'react';
import Header from './components/Header';
import TabNavigation from './components/TabNavigation';
import TranscribeTab from './components/TranscribeTab';
import ModelsTab from './components/ModelsTab';
import Toast from './components/Toast';
import { apiService } from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState('transcribe');
  const [apiStatus, setApiStatus] = useState({ online: false, checking: true });
  const [toast, setToast] = useState(null);
  const [models, setModels] = useState([]);
  const [loadedCount, setLoadedCount] = useState(0);

  useEffect(() => {
    console.log('🚀 App mounted - Initializing API connections...');
    checkApiHealth();
    loadModels();
  }, []);

  const checkApiHealth = async () => {
    console.log('🔍 Checking API health...');
    setApiStatus({ online: false, checking: true });
    
    try {
      const data = await apiService.checkHealth();
      console.log('✅ Health check response:', data);
      
      const isHealthy = data && data.status === 'healthy';
      console.log('Health status:', isHealthy ? '🟢 ONLINE' : '🔴 OFFLINE');
      
      setApiStatus({ 
        online: isHealthy, 
        checking: false 
      });
      
      if (isHealthy) {
        console.log('✨ Backend is online and ready!');
      }
    } catch (error) {
      console.error('❌ Health check failed:', error);
      console.error('Error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status
      });
      setApiStatus({ online: false, checking: false });
    }
  };

  const loadModels = async () => {
    console.log('📦 Loading models list...');
    try {
      const data = await apiService.getRegistryModels();
      console.log('Models response:', data);
      if (data.success) {
        console.log(`✅ Loaded ${data.models.length} models (${data.loaded_count} in memory)`);
        setModels(data.models);
        setLoadedCount(data.loaded_count);
      }
    } catch (error) {
      console.error('❌ Error loading models:', error);
    }
  };

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 5000);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-slate-900 text-gray-900 dark:text-gray-100">
      <Header apiStatus={apiStatus} />
      
      <main className="container mx-auto px-4 py-6 max-w-5xl">
        <TabNavigation activeTab={activeTab} setActiveTab={setActiveTab} />
        
        {activeTab === 'transcribe' ? (
          <TranscribeTab 
            models={models}
            loadedCount={loadedCount}
            showToast={showToast}
          />
        ) : (
          <ModelsTab 
            models={models}
            loadModels={loadModels}
            showToast={showToast}
          />
        )}
      </main>

      <footer className="bg-white dark:bg-slate-800 mt-8 py-4 border-t border-gray-200 dark:border-gray-700">
        <div className="container mx-auto px-4 text-center">
          <div className="flex justify-center items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
            <span>Powered by HuggingFace & FastAPI</span>
            <span>•</span>
            <a 
              href="http://localhost:8000/docs" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-600 dark:text-blue-400 hover:underline"
            >
              API Docs
            </a>
          </div>
        </div>
      </footer>

      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  );
}

export default App;
