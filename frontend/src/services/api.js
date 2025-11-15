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
    const response = await api.post('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  list: async (skip = 0, limit = 100) => {
    const response = await api.get(`/api/documents/?skip=${skip}&limit=${limit}`);
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
    const response = await api.post(`/api/extraction/process/${documentId}`, null, {
      params: { ocr_engine: ocrEngine },
    });
    return response.data;
  },

  getByDocument: async (documentId) => {
    const response = await api.get(`/api/extraction/document/${documentId}`);
    return response.data;
  },

  get: async (id) => {
    const response = await api.get(`/api/extraction/${id}`);
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.put(`/api/extraction/${id}`, data);
    return response.data;
  },
};

// Learning API
export const learningAPI = {
  recordCorrection: async (data) => {
    const response = await api.post('/api/learning/corrections', data);
    return response.data;
  },

  getCorrections: async (fieldName, limit = 10) => {
    const response = await api.get(`/api/learning/corrections/${fieldName}`, {
      params: { limit },
    });
    return response.data;
  },

  getStats: async () => {
    const response = await api.get('/api/learning/stats');
    return response.data;
  },
};

export default api;
