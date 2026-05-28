import axios from 'axios';

// Configuración base de axios
const API_BASE_URL = 'http://localhost:8000/api';

const servicioApi = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Helper para emitir eventos de notificación
const emitApiEvent = (type, detail) => {
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new CustomEvent(type, { detail }));
  }
};

// Interceptor para incluir token JWT
servicioApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores de autenticación y notificaciones
servicioApi.interceptors.response.use(
  (response) => {
    emitApiEvent('api-success', {
      status: response.status,
      method: response.config?.method,
      url: response.config?.url,
    });
    return response;
  },
  (error) => {
    const status = error.response?.status;
    const data = error.response?.data;
    const url = error.config?.url || '';

    emitApiEvent('api-error', {
      status,
      data,
      url,
    });

    if (status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }

    return Promise.reject(error);
  }
);

export default servicioApi;
