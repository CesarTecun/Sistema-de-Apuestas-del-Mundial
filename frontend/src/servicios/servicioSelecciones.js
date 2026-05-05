import servicioApi from './servicioApi';

export const servicioSelecciones = {
  // Obtener todas las selecciones
  getSelecciones: async () => {
    try {
      const response = await servicioApi.get('/partidos/selecciones/');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener selecciones:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar selecciones';
      return { success: false, error: errorMessage };
    }
  },

  // Obtener selección por ID
  getSeleccion: async (id) => {
    try {
      const response = await servicioApi.get(`/partidos/selecciones/${id}/`);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener selección:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar selección';
      return { success: false, error: errorMessage };
    }
  },

  // Crear selección
  createSeleccion: async (seleccionData) => {
    try {
      const response = await servicioApi.post('/partidos/selecciones/', seleccionData);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al crear selección:', error);
      const errorMessage = error.response?.data?.detail || 'Error al crear selección';
      return { success: false, error: errorMessage };
    }
  },

  // Actualizar selección
  updateSeleccion: async (id, seleccionData) => {
    try {
      const response = await servicioApi.put(`/partidos/selecciones/${id}/`, seleccionData);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al actualizar selección:', error);
      const errorMessage = error.response?.data?.detail || 'Error al actualizar selección';
      return { success: false, error: errorMessage };
    }
  },

  // Eliminar selección
  deleteSeleccion: async (id) => {
    try {
      await servicioApi.delete(`/partidos/selecciones/${id}/`);
      return { success: true };
    } catch (error) {
      console.error('Error al eliminar selección:', error);
      const errorMessage = error.response?.data?.detail || 'Error al eliminar selección';
      return { success: false, error: errorMessage };
    }
  }
};

export default servicioSelecciones;
