import servicioApi from './servicioApi';

const servicioLigas = {
  async getLigas() {
    try {
      const response = await servicioApi.get('/ligas/');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener ligas:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar ligas';
      return { success: false, error: errorMessage };
    }
  },

  async getParticipantes(ligaId) {
    try {
      const url = ligaId ? `/ligas/participantes/por-liga/?fk_id_liga=${ligaId}` : '/ligas/participantes/por-liga/';
      const response = await servicioApi.get(url);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener participantes:', error);
      // Fallback al endpoint original si el nuevo endpoint no está disponible (404)
      if (error.response?.status === 404) {
        console.warn('Endpoint participantes/por-liga no disponible, usando fallback');
        try {
          const fallbackUrl = ligaId ? `/ligas/participantes/?fk_id_liga=${ligaId}` : '/ligas/participantes/';
          const fallbackResponse = await servicioApi.get(fallbackUrl);
          return { success: true, data: fallbackResponse.data };
        } catch (fallbackError) {
          const errorMessage = fallbackError.response?.data?.detail || fallbackError.response?.data?.error || 'Error al cargar participantes';
          return { success: false, error: errorMessage };
        }
      }
      const errorMessage = error.response?.data?.detail || error.response?.data?.error || 'Error al cargar participantes';
      return { success: false, error: errorMessage };
    }
  },

  async enviarInvitacion(ligaId, data) {
    try {
      const response = await servicioApi.post(`/ligas/${ligaId}/enviar-invitacion/`, data);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al enviar invitación:', error);
      const errorMessage = error.response?.data?.detail || 'Error al enviar invitación';
      return { success: false, error: errorMessage };
    }
  },

  async getInvitaciones(ligaId) {
    try {
      const url = ligaId ? `/ligas/invitaciones/?fk_id_liga=${ligaId}` : '/ligas/invitaciones/';
      console.log('[servicioLigas] Obteniendo invitaciones de:', url);
      const response = await servicioApi.get(url);
      console.log('[servicioLigas] Respuesta de invitaciones:', response.data);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener invitaciones:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar invitaciones';
      return { success: false, error: errorMessage };
    }
  },
};

export default servicioLigas;
