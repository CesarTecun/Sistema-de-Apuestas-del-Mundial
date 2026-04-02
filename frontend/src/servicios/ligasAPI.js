import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const ligasAPI = {
  // Obtener todas las ligas
  getLigas: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/ligas/api/ligas/`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener ligas:', error);
      throw error;
    }
  },

  // Obtener una liga específica
  getLiga: async (id) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/ligas/api/ligas/${id}/`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener liga:', error);
      throw error;
    }
  },

  // Crear una nueva liga
  createLiga: async (ligaData) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/ligas/api/ligas/`, ligaData);
      return response.data;
    } catch (error) {
      console.error('Error al crear liga:', error);
      throw error;
    }
  },

  // Actualizar una liga existente
  updateLiga: async (id, ligaData) => {
    try {
      const response = await axios.put(`${API_BASE_URL}/api/ligas/api/ligas/${id}/`, ligaData);
      return response.data;
    } catch (error) {
      console.error('Error al actualizar liga:', error);
      throw error;
    }
  },

  // Eliminar una liga
  deleteLiga: async (id) => {
    try {
      const response = await axios.delete(`${API_BASE_URL}/api/ligas/api/ligas/${id}/`);
      return response.data;
    } catch (error) {
      console.error('Error al eliminar liga:', error);
      throw error;
    }
  },

  // Obtener ligas por usuario administrador
  getLigasPorUsuario: async (usuarioId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/ligas/api/ligas/por-usuario/?usuario_id=${usuarioId}`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener ligas del usuario:', error);
      throw error;
    }
  }
};

export default ligasAPI;
