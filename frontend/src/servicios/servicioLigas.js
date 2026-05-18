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
};

export default servicioLigas;
