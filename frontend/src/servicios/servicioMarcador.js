import servicioApi from './servicioApi';

export const servicioMarcador = {
  // Health check del microservicio
  healthCheck: async () => {
    try {
      const response = await servicioApi.get('/partidos/marcador/health/');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al verificar microservicio marcador:', error);
      return { success: false, error: 'Microservicio marcador no disponible' };
    }
  },

  // Obtener selecciones del microservicio marcador
  getSelecciones: async () => {
    try {
      const response = await servicioApi.get('/partidos/marcador/selecciones/');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener selecciones del marcador:', error);
      return { success: false, error: error.response?.data?.detail || 'Error al cargar selecciones' };
    }
  },

  // Obtener todos los partidos del microservicio marcador
  getPartidos: async (estado, fkIdLiga) => {
    try {
      const params = {};
      if (estado) params.estado = estado;
      if (fkIdLiga) params.fk_id_liga = fkIdLiga;
      const response = await servicioApi.get('/partidos/marcador/partidos/', { params });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener partidos del marcador:', error);
      return { success: false, error: error.response?.data?.detail || 'Error al cargar partidos' };
    }
  },

  // Obtener partidos en vivo (en juego) del microservicio marcador
  getPartidosEnVivo: async () => {
    try {
      const response = await servicioApi.get('/partidos/marcador/partidos/en-vivo/');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener partidos en vivo:', error);
      return { success: false, error: error.response?.data?.detail || 'Error al cargar partidos en vivo' };
    }
  },

  // Obtener detalle de un partido del microservicio marcador
  getPartido: async (id) => {
    try {
      const response = await servicioApi.get(`/partidos/marcador/partidos/${id}/`);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener partido del marcador:', error);
      return { success: false, error: error.response?.data?.detail || 'Error al cargar partido' };
    }
  },

  // Obtener partidos por equipo del microservicio marcador
  getPartidosPorEquipo: async (equipoId) => {
    try {
      const response = await servicioApi.get('/partidos/marcador/partidos/por-equipo/', {
        params: { equipo_id: equipoId }
      });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener partidos por equipo del marcador:', error);
      return { success: false, error: error.response?.data?.detail || 'Error al cargar partidos del equipo' };
    }
  },

  // Crear partido en el microservicio marcador
  createPartido: async (partidoData) => {
    try {
      const response = await servicioApi.post('/partidos/marcador/partidos/crear/', partidoData);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al crear partido en marcador:', error);
      return { success: false, error: error.response?.data?.detail || 'Error al crear partido' };
    }
  },

  // Actualizar partido en el microservicio marcador
  updatePartido: async (id, partidoData) => {
    try {
      const response = await servicioApi.patch(`/partidos/marcador/partidos/${id}/actualizar/`, partidoData);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al actualizar partido en marcador:', error);
      return { success: false, error: error.response?.data?.detail || 'Error al actualizar partido' };
    }
  },

  // Actualizar marcador de un partido en el microservicio marcador
  actualizarMarcador: async (id, golLocal, golVisitante, estado, resultado, ganadorPenales, faltasLocal, faltasVisitante) => {
    try {
      const payload = {};
      if (golLocal !== undefined && golLocal !== null) payload.gol_local = golLocal;
      if (golVisitante !== undefined && golVisitante !== null) payload.gol_visitante = golVisitante;
      if (estado !== undefined && estado !== null) payload.estado = estado;
      if (resultado !== undefined && resultado !== null) payload.resultado = resultado;
      if (ganadorPenales !== undefined && ganadorPenales !== null) payload.ganador_penales = ganadorPenales;
      if (faltasLocal !== undefined && faltasLocal !== null) payload.faltas_local = faltasLocal;
      if (faltasVisitante !== undefined && faltasVisitante !== null) payload.faltas_visitante = faltasVisitante;

      const response = await servicioApi.post(`/partidos/marcador/partidos/${id}/actualizar-marcador/`, payload);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al actualizar marcador:', error);
      return { success: false, error: error.response?.data?.detail || 'Error al actualizar marcador' };
    }
  },

  // Controlar partido (iniciar, pausar, cambiar tiempo, etc.)
  controlarPartido: async (id, controlData) => {
    try {
      const response = await servicioApi.patch(`/partidos/marcador/partidos/${id}/control/`, controlData);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al controlar partido:', error);
      return { success: false, error: error.response?.data?.detail || 'Error al controlar partido' };
    }
  },

  // Eliminar partido del microservicio marcador
  deletePartido: async (id) => {
    try {
      await servicioApi.delete(`/partidos/marcador/partidos/${id}/eliminar/`);
      return { success: true };
    } catch (error) {
      console.error('Error al eliminar partido del marcador:', error);
      return { success: false, error: error.response?.data?.detail || 'Error al eliminar partido' };
    }
  }
};

export default servicioMarcador;
