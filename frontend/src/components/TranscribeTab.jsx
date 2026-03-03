import { useState, useEffect } from 'react';
import FileUpload from './FileUpload';
import TranscriptionResults from './TranscriptionResults';
import LoadingSpinner from './LoadingSpinner';
import { apiService } from '../services/api';

const TranscribeTab = ({ models, loadedCount, showToast }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedModel, setSelectedModel] = useState('');
  const [enableDiarization, setEnableDiarization] = useState(true);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [modelCapabilities, setModelCapabilities] = useState(null);
  const [loadingCapabilities, setLoadingCapabilities] = useState(false);

  const loadedModels = models.filter(m => m.is_loaded);

  // Fetch model capabilities when selected model changes
  useEffect(() => {
    const fetchCapabilities = async () => {
      if (!selectedModel) {
        setModelCapabilities(null);
        return;
      }

      setLoadingCapabilities(true);
      try {
        const data = await apiService.getModelCapabilities(selectedModel);
        if (data.success && data.capabilities) {
          setModelCapabilities(data.capabilities);
        }
      } catch (error) {
        console.error('Failed to fetch model capabilities:', error);
        // Use fallback from models list if API call fails
        const model = models.find(m => m.model_id === selectedModel);
        if (model) {
          setModelCapabilities({
            supports_diarization: model.supports_diarization,
            supports_timestamps: model.supports_timestamps,
            model_type: model.model_type,
          });
        }
      } finally {
        setLoadingCapabilities(false);
      }
    };

    fetchCapabilities();
  }, [selectedModel, models]);

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setResults(null);
  };

  const handleTranscribe = async () => {
    if (!selectedFile) {
      showToast('Please select an audio file first.', 'error');
      return;
    }

    if (!selectedModel) {
      showToast('Please select a model for transcription.', 'error');
      return;
    }

    setLoading(true);
    setResults(null);

    try {
      const data = await apiService.transcribeAudio(selectedFile, selectedModel, enableDiarization);
      
      if (data.success) {
        setResults(data);
        showToast('Transcription completed successfully!', 'success');
      } else {
        throw new Error(data.error || 'Transcription failed');
      }
    } catch (error) {
      console.error('Transcription error:', error);
      let errorMessage = 'Transcription failed';
      
      if (error.message) {
        errorMessage = error.message.includes('timeout') 
          ? 'Request timed out. Please try again with a shorter audio file.'
          : `Transcription failed: ${error.message}`;
      }
      
      showToast(errorMessage, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* Header Info */}
      <div className="card">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-base font-semibold text-gray-800 dark:text-gray-100">
            Audio Transcription
          </h2>
          <div className="flex gap-4 text-xs text-gray-600 dark:text-gray-400">
            <span>Formats: WAV, MP3, FLAC, M4A, OGG</span>
            <span>•</span>
            <span>Max: 25MB</span>
            <span>•</span>
            <span>Models: {loadedCount}</span>
          </div>
        </div>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Convert audio files to text using AI models. Select a model and upload your file to begin.
        </p>
      </div>

      {/* Main Upload Card */}
      <div className="card">
        {/* Model Selection */}
        <div className="mb-4">
          <label htmlFor="model-select" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Select Model <span className="text-red-500">*</span>
          </label>
          <select 
            id="model-select" 
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            disabled={loadedModels.length === 0}
            className="input-field"
          >
            <option value="">
              {loadedModels.length === 0 
                ? 'No models loaded - Go to Model Management to load models'
                : 'Choose a model...'}
            </option>
            {loadedModels.map((model) => (
              <option key={model.model_id} value={model.model_id}>
                {model.model_id}
              </option>
            ))}
          </select>

          {/* Model Type Info */}
          {selectedModel && modelCapabilities && !loadingCapabilities && (
            <div className="mt-2 flex gap-1.5 flex-wrap">
              <span className="text-xs text-gray-600 dark:text-gray-400 mr-1">Model type:</span>
              <span className="px-2 py-0.5 bg-gray-50 dark:bg-gray-800/50 text-gray-700 dark:text-gray-300 text-xs rounded border border-gray-200 dark:border-gray-700 font-medium">
                {modelCapabilities.model_type}
              </span>
            </div>
          )}
          {loadingCapabilities && (
            <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
              Loading model info...
            </div>
          )}
        </div>

        {/* Diarization Option */}
        <div className="mb-4">
          <label className="flex items-center space-x-2 cursor-pointer">
            <input
              type="checkbox"
              checked={enableDiarization}
              onChange={(e) => setEnableDiarization(e.target.checked)}
              className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
            />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Enable Speaker Diarization
            </span>
          </label>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 ml-6">
            Identify different speakers using pyannote/speaker-diarization-3.1 (works with all models)
          </p>
        </div>

        {/* File Upload */}
        <FileUpload 
          onFileSelect={handleFileSelect}
          selectedFile={selectedFile}
          onTranscribe={handleTranscribe}
          disabled={!selectedModel || loading}
        />
      </div>

      {/* Loading State */}
      {loading && (
        <div className="card">
          <LoadingSpinner 
            message="Processing audio transcription..." 
            subMessage="This may take several minutes for large files. Please wait..." 
          />
        </div>
      )}

      {/* Results */}
      {results && !loading && (
        <TranscriptionResults results={results} showToast={showToast} />
      )}
    </div>
  );
};

export default TranscribeTab;
