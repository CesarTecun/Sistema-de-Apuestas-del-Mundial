// Configuración centralizada de la API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  // Autenticación
  AUTH: {
    LOGIN: `${API_BASE_URL}/api/auth/login/`,
    LOGOUT: `${API_BASE_URL}/api/auth/logout/`,
    PROFILE: `${API_BASE_URL}/api/auth/profile/`,
    TOKEN: `${API_BASE_URL}/api/token/`,
    TOKEN_REFRESH: `${API_BASE_URL}/api/token/refresh/`,
    PASSWORD_RESET_REQUEST: `${API_BASE_URL}/api/auth/password/reset/`,
    PASSWORD_RESET_CONFIRM: `${API_BASE_URL}/api/auth/password/reset/confirm/`,
  },
  // Ligas
  LIGAS: `${API_BASE_URL}/api/ligas/`,
  // Partidos
  PARTIDOS: `${API_BASE_URL}/api/partidos/`,
  // Pronósticos
  PRONOSTICOS: `${API_BASE_URL}/api/pronosticos/`,
  // Posiciones
  POSICIONES: `${API_BASE_URL}/api/posiciones/`,
  // Premios
  PREMIOS: `${API_BASE_URL}/api/premios/`,
  // Historial
  HISTORIAL: `${API_BASE_URL}/api/historial/`,
  // Core (sedes, fases)
  CORE: `${API_BASE_URL}/api/core/`,
  SEDES: `${API_BASE_URL}/api/core/sedes/`,
};

export const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : '',
  };
};

export default API_ENDPOINTS;
