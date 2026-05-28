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
      const url = ligaId ? `/ligas/participantes/?fk_id_liga=${ligaId}` : '/ligas/participantes/';
      const response = await servicioApi.get(url);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener participantes:', error);
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
      const response = await servicioApi.get(`/ligas/invitaciones/?fk_id_liga=${ligaId}`);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Error al obtener invitaciones:', error);
      const errorMessage = error.response?.data?.detail || 'Error al cargar invitaciones';
      return { success: false, error: errorMessage };
    }
  },
};

export default servicioLigas;
