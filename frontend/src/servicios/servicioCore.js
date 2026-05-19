import API_ENDPOINTS, { getAuthHeaders } from '../config/apiConfig';

const servicioCore = {
  getSedes: async () => {
    try {
      const response = await fetch(API_ENDPOINTS.SEDES, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('Error al obtener sedes:', error);
      return { success: false, error: error.message || 'Error al obtener sedes' };
    }
  },

  getFases: async () => {
    try {
      const response = await fetch(`${API_ENDPOINTS.CORE}fases/`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('Error al obtener fases:', error);
      return { success: false, error: error.message || 'Error al obtener fases' };
    }
  }
};

export default servicioCore;
