import servicioApi from './servicioApi';

export const servicioHistorial = {
  // Obtener historial completo de pronósticos del usuario autenticado
  getHistorialUsuario: async () => {
    try {
      const response = await servicioApi.get('/pronosticos/mi-historial/');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener historial:', error);
      return { success: false, error: error.response?.data?.detail || 'Error al cargar el historial' };
    }
  }
};

export default servicioHistorial;
