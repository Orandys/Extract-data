import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Documents API
export const documentsAPI = {
  upload: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/api/documents', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  get: async (id) => {
    const response = await api.get(`/api/documents/${id}`);
    return response.data;
  },

  delete: async (id) => {
    const response = await api.delete(`/api/documents/${id}`);
    return response.data;
  },
};

// Extraction API
export const extractionAPI = {
  process: async (documentId, ocrEngine = 'tesseract') => {
    const response = await api.post(
      `/api/extraction/process/${documentId}`,
      null,
      { params: { ocr_engine: ocrEngine } }
    );
    return response.data;
  },

  getByDocument: async (documentId) => {
    const response = await api.get(`/api/extraction/document/${documentId}`);
    return response.data;
  },
};

// Corrections API
export const correctionsAPI = {
  save: async (data) => {
    const response = await api.post('/api/corrections', data);
    return response.data;
  },
};

// Metrics API
export const metricsAPI = {
  getAll: async () => {
    const response = await api.get('/api/metrics');
    return response.data;
  },
};

// Health check
export const healthCheck = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

export default api;
