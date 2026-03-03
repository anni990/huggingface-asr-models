import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second default timeout
});

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.config.url, response.status);
    return response;
  },
  (error) => {
    console.error('API Error:', error.config?.url, error.message);
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
    } else if (error.code === 'ECONNABORTED') {
      console.error('Request timeout - operation took too long');
    } else if (error.message.includes('timeout')) {
      console.error('Request timeout - the server is taking longer than expected');
    }
    return Promise.reject(error);
  }
);

export const apiService = {
  // Health Check
  checkHealth: async () => {
    try {
      const response = await api.get('/health', {
        timeout: 5000, // 5 seconds for health check
      });
      return response.data;
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  },

  // Transcription
  transcribeAudio: async (file, modelId, enableDiarization = true) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('model_id', modelId);
    formData.append('diarization', enableDiarization);

    const response = await api.post('/api/v1/transcription/transcribe', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 600000, // 10 minutes for transcription - AI processing takes time
    });
    return response.data;
  },

  // Model Management
  getRegistryModels: async () => {
    const response = await api.get('/api/v1/transcription/models/registry');
    return response.data;
  },

  getLoadedModels: async () => {
    const response = await api.get('/api/v1/transcription/models/loaded');
    return response.data;
  },

  getRecommendedModels: async () => {
    const response = await api.get('/api/v1/transcription/models/recommended');
    return response.data;
  },

  loadModel: async (modelId) => {
    const formData = new FormData();
    formData.append('model_id', modelId);

    const response = await api.post('/api/v1/transcription/models/load', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 300000, // 5 minutes for model loading - downloading models takes time
    });
    return response.data;
  },

  unloadModel: async (modelId) => {
    const formData = new FormData();
    formData.append('model_id', modelId);

    const response = await api.delete('/api/v1/transcription/models/unload', {
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  deleteModel: async (modelId) => {
    const formData = new FormData();
    formData.append('model_id', modelId);

    const response = await api.delete('/api/v1/transcription/models/delete', {
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get model capabilities
  getModelCapabilities: async (modelId) => {
    const response = await api.get(`/api/v1/transcription/models/capabilities/${encodeURIComponent(modelId)}`);
    return response.data;
  },
};

export default api;
