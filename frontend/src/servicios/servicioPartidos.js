import servicioApi from './servicioApi';

export const servicioPartidos = {
  // Obtener todos los partidos
  getPartidos: async () => {
    try {
      const response = await servicioApi.get('/partidos/partidos/');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener partidos:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar partidos';
      return { success: false, error: errorMessage };
    }
  },

  // Obtener partido por ID
  getPartido: async (id) => {
    try {
      const response = await servicioApi.get(`/partidos/partidos/${id}/`);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener partido:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar partido';
      return { success: false, error: errorMessage };
    }
  },

  // Crear partido
  createPartido: async (partidoData) => {
    try {
      const response = await servicioApi.post('/partidos/partidos/', partidoData);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al crear partido:', error);
      const errorMessage = error.response?.data?.detail || 'Error al crear partido';
      return { success: false, error: errorMessage };
    }
  },

  // Actualizar partido
  updatePartido: async (id, partidoData) => {
    try {
      const response = await servicioApi.put(`/partidos/partidos/${id}/`, partidoData);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al actualizar partido:', error);
      const errorMessage = error.response?.data?.detail || 'Error al actualizar partido';
      return { success: false, error: errorMessage };
    }
  },

  // Eliminar partido
  deletePartido: async (id) => {
    try {
      await servicioApi.delete(`/partidos/partidos/${id}/`);
      return { success: true };
    } catch (error) {
      console.error('Error al eliminar partido:', error);
      const errorMessage = error.response?.data?.detail || 'Error al eliminar partido';
      return { success: false, error: errorMessage };
    }
  },

  // Actualizar resultado de partido
  actualizarResultado: async (id, golLocal, golVisitante, resultado) => {
    try {
      const response = await servicioApi.post(`/partidos/partidos/${id}/actualizar-resultado/`, {
        gol_local: golLocal,
        gol_visitante: golVisitante,
        resultado: resultado
      });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al actualizar resultado:', error);
      const errorMessage = error.response?.data?.detail || 'Error al actualizar resultado';
      return { success: false, error: errorMessage };
    }
  },

  // Obtener partidos por liga
  getPartidosPorLiga: async (ligaId) => {
    try {
      const response = await servicioApi.get('/partidos/partidos/por-liga/', {
        params: { liga_id: ligaId }
      });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener partidos por liga:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar partidos de la liga';
      return { success: false, error: errorMessage };
    }
  },

  // Obtener partidos por equipo
  getPartidosPorEquipo: async (equipoId) => {
    try {
      const response = await servicioApi.get('/partidos/partidos/por-equipo/', {
        params: { equipo_id: equipoId }
      });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener partidos por equipo:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar partidos del equipo';
      return { success: false, error: errorMessage };
    }
  },

  // Obtener selecciones
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

  // Obtener jugadores
  getJugadores: async () => {
    try {
      const response = await servicioApi.get('/partidos/jugadores/');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener jugadores:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar jugadores';
      return { success: false, error: errorMessage };
    }
  },

  // Obtener jugadores por selección
  getJugadoresPorSeleccion: async (seleccionId) => {
    try {
      const response = await servicioApi.get('/partidos/jugadores/', {
        params: { fk_id_seleccion: seleccionId }
      });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener jugadores por selección:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar jugadores de la selección';
      return { success: false, error: errorMessage };
    }
  }
};

export default servicioPartidos;
