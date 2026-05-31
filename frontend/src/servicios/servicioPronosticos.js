import servicioApi from './servicioApi';

const servicioPronosticos = {
  async getPronosticos() {
    try {
      const response = await servicioApi.get('/pronosticos/pronosticos/');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener pronósticos:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar pronósticos';
      return { success: false, error: errorMessage };
    }
  },

  async getPronostico(id) {
    try {
      const response = await servicioApi.get(`/pronosticos/pronosticos/${id}/`);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener pronóstico:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar pronóstico';
      return { success: false, error: errorMessage };
    }
  },

  async crearPronostico(data) {
    try {
      const response = await servicioApi.post('/pronosticos/pronosticos/', data);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al crear pronóstico:', error);
      const errorMessage = error.response?.data?.detail || 'Error al crear pronóstico';
      return { success: false, error: errorMessage };
    }
  },

  async actualizarPronostico(id, data) {
    try {
      const response = await servicioApi.put(`/pronosticos/pronosticos/${id}/`, data);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al actualizar pronóstico:', error);
      const errorMessage = error.response?.data?.detail || 'Error al actualizar pronóstico';
      return { success: false, error: errorMessage };
    }
  },

  async eliminarPronostico(id) {
    try {
      const response = await servicioApi.delete(`/pronosticos/pronosticos/${id}/`);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al eliminar pronóstico:', error);
      const errorMessage = error.response?.data?.detail || 'Error al eliminar pronóstico';
      return { success: false, error: errorMessage };
    }
  },

  async getPronosticosPorUsuario(usuarioId) {
    try {
      const response = await servicioApi.get('/pronosticos/por-usuario/', { params: { usuario_id: usuarioId } });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener pronósticos del usuario:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar pronósticos del usuario';
      return { success: false, error: errorMessage };
    }
  },

  async getPronosticosPorLiga(ligaId) {
    try {
      const response = await servicioApi.get('/pronosticos/por-liga/', { params: { liga_id: ligaId } });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener pronósticos de la liga:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar pronósticos de la liga';
      return { success: false, error: errorMessage };
    }
  },

  async getPronosticosPorPartido(partidoId) {
    try {
      const response = await servicioApi.get('/pronosticos/por-partido/', { params: { partido_id: partidoId } });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener pronósticos del partido:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar pronósticos del partido';
      return { success: false, error: errorMessage };
    }
  },

  async getPronosticosPorPartidoLiga(partidoId, ligaId) {
    try {
      const response = await servicioApi.get('/pronosticos/por-partido-liga/', { params: { partido_id: partidoId, liga_id: ligaId } });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener pronósticos del partido por liga:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar pronósticos del partido por liga';
      return { success: false, error: errorMessage };
    }
  },

  async getPronosticosUsuarioLiga(usuarioId, ligaId) {
    try {
      const response = await servicioApi.get('/pronosticos/usuario-liga/', { params: { usuario_id: usuarioId, liga_id: ligaId } });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener pronósticos del usuario en la liga:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar pronósticos del usuario en la liga';
      return { success: false, error: errorMessage };
    }
  },

  async verificarPronosticoDisponible(usuarioId, partidoId, ligaId) {
    try {
      const response = await servicioApi.post('/pronosticos/verificar-disponible/', { usuario_id: usuarioId, partido_id: partidoId, liga_id: ligaId });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al verificar disponibilidad de pronóstico:', error);
      const errorMessage = error.response?.data?.detail || 'Error al verificar disponibilidad';
      return { success: false, error: errorMessage };
    }
  },

  async getHistorialUsuario() {
    try {
      const response = await servicioApi.get('/pronosticos/mi-historial/');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener historial del usuario:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar historial';
      return { success: false, error: errorMessage };
    }
  },
};

export default servicioPronosticos;
