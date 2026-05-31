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
  },

  // Obtener todos los pronósticos de los partidos del usuario (incluyendo otros usuarios)
  getPronosticosPartidosUsuario: async () => {
    try {
      const response = await servicioApi.get('/pronosticos/partidos-usuario/');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener pronósticos de partidos:', error);
      return { success: false, error: error.response?.data?.detail || 'Error al cargar pronósticos de partidos' };
    }
  }
};

export default servicioHistorial;
