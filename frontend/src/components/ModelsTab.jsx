import { useState, useEffect } from 'react';
import ModelsList from './ModelsList';
import LoadingSpinner from './LoadingSpinner';
import { apiService } from '../services/api';

const ModelsTab = ({ models, loadModels, showToast }) => {
  const [newModelId, setNewModelId] = useState('');
  const [recommendedModels, setRecommendedModels] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadRecommendedModels();
  }, []);

  const loadRecommendedModels = async () => {
    try {
      const data = await apiService.getRecommendedModels();
      if (data.success) {
        setRecommendedModels(data.recommended_models);
      }
    } catch (error) {
      console.error('Error loading recommended models:', error);
    }
  };

  const handleLoadModel = async () => {
    const modelId = newModelId.trim();
    
    if (!modelId) {
      showToast('Please enter a model ID', 'error');
      return;
    }

    setLoading(true);

    try {
      const data = await apiService.loadModel(modelId);
      
      if (data.success) {
        showToast(`Model ${modelId} loaded successfully!`, 'success');
        setNewModelId('');
        await loadModels();
      } else {
        throw new Error(data.message || 'Failed to load model');
      }
    } catch (error) {
      console.error('Error loading model:', error);
      showToast(`Failed to load model: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadModelById = async (modelId) => {
    setLoading(true);
    try {
      const data = await apiService.loadModel(modelId);
      
      if (data.success) {
        showToast(`Model ${modelId} loaded successfully!`, 'success');
        await loadModels();
      } else {
        throw new Error(data.message || 'Failed to load model');
      }
    } catch (error) {
      console.error('Error loading model:', error);
      showToast(`Failed to load model: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleUnloadModel = async (modelId) => {
    setLoading(true);
    try {
      const data = await apiService.unloadModel(modelId);
      
      if (data.success) {
        showToast(`Model ${modelId} unloaded from memory`, 'success');
        await loadModels();
      } else {
        showToast(data.message || 'Failed to unload model', 'error');
      }
    } catch (error) {
      console.error('Error unloading model:', error);
      showToast(`Failed to unload model: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteModel = async (modelId) => {
    if (!window.confirm(`Are you sure you want to delete model "${modelId}"? This will remove it from the registry and unload from memory.`)) {
      return;
    }

    setLoading(true);
    try {
      const data = await apiService.deleteModel(modelId);
      
      if (data.success) {
        showToast(`Model ${modelId} deleted successfully`, 'success');
        await loadModels();
      } else {
        showToast(data.message || 'Failed to delete model', 'error');
      }
    } catch (error) {
      console.error('Error deleting model:', error);
      showToast(`Failed to delete model: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* Load Model Card */}
      <div className="card">
        <h2 className="text-base font-semibold text-gray-800 dark:text-gray-100 mb-3">
          Load New Model
        </h2>
        
        <div className="flex gap-2">
          <input 
            type="text" 
            value={newModelId}
            onChange={(e) => setNewModelId(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleLoadModel()}
            placeholder="e.g., openai/whisper-large-v3"
            disabled={loading}
            className="input-field flex-1"
          />
          <button 
            onClick={handleLoadModel}
            disabled={loading}
            className="btn-primary"
          >
            {loading ? 'Loading...' : 'Load Model'}
          </button>
        </div>
        
        {recommendedModels.length > 0 && (
          <div className="mt-3">
            <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-2">Recommended:</p>
            <div className="flex flex-wrap gap-2">
              {recommendedModels.map((modelId) => (
                <button
                  key={modelId}
                  onClick={() => setNewModelId(modelId)}
                  disabled={loading}
                  className="px-2 py-1 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs rounded hover:bg-blue-100 dark:hover:bg-blue-900/50 transition-colors border border-blue-200 dark:border-blue-800"
                >
                  {modelId}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Models List Card */}
      <div className="card">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-base font-semibold text-gray-800 dark:text-gray-100">
            Registered Models
          </h2>
          <button 
            onClick={loadModels}
            disabled={loading}
            className="btn-secondary text-xs"
          >
            Refresh
          </button>
        </div>
        
        {loading ? (
          <LoadingSpinner message="Loading models..." />
        ) : (
          <ModelsList 
            models={models}
            onLoad={handleLoadModelById}
            onUnload={handleUnloadModel}
            onDelete={handleDeleteModel}
          />
        )}
      </div>
    </div>
  );
};

export default ModelsTab;
