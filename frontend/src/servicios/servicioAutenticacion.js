import servicioApi from './servicioApi';

export const servicioAutenticacion = {
  // Login
  login: async (email, password) => {
    try {
      // Login tradicional
      const loginResponse = await servicioApi.post('/auth/login/', { email, password });
      
      // Obtener tokens JWT
      const tokenResponse = await servicioApi.post('/token/', { email, password });
      
      const { access, refresh } = tokenResponse.data;
      
      // Guardar tokens
      localStorage.setItem('token', access);
      localStorage.setItem('refreshToken', refresh);
      
      return {
        success: true,
        user: loginResponse.data.user,
        tokens: { access, refresh }
      };
    } catch (error) {
      console.error('Error de login:', error);
      const errorMessage = error.response?.data?.non_field_errors?.[0] || 
                          error.response?.data?.detail || 
                          'Error al iniciar sesión';
      return { success: false, error: errorMessage };
    }
  },

  // Registro
  register: async (userData) => {
    try {
      const response = await servicioApi.post('/auth/register/', userData);
      
      // Obtener tokens después del registro
      const tokenResponse = await servicioApi.post('/token/', {
        email: userData.email,
        password: userData.password
      });

      const { access, refresh } = tokenResponse.data;
      
      // Guardar tokens
      localStorage.setItem('token', access);
      localStorage.setItem('refreshToken', refresh);
      
      return {
        success: true,
        user: response.data.user,
        tokens: { access, refresh }
      };
    } catch (error) {
      console.error('Error de registro:', error);
      const errorMessage = error.response?.data?.email?.[0] || 
                          error.response?.data?.password?.[0] || 
                          error.response?.data?.detail || 
                          'Error al registrar usuario';
      return { success: false, error: errorMessage };
    }
  },

  // Logout
  logout: async () => {
    try {
      await servicioApi.post('/auth/logout/');
    } catch (error) {
      console.error('Error de logout:', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
    }
  },

  // Verificar autenticación
  checkAuth: async () => {
    try {
      const response = await servicioApi.get('/auth/check/');
      return {
        success: true,
        isAuthenticated: response.data.is_authenticated,
        user: response.data.user
      };
    } catch (error) {
      return { success: false, isAuthenticated: false };
    }
  },

  // Refresh token
  refreshToken: async () => {
    try {
      const refreshToken = localStorage.getItem('refreshToken');
      if (!refreshToken) {
        throw new Error('No refresh token disponible');
      }

      const response = await servicioApi.post('/token/refresh/', {
        refresh: refreshToken
      });

      const { access } = response.data;
      localStorage.setItem('token', access);
      
      return { success: true, token: access };
    } catch (error) {
      console.error('Error refrescando token:', error);
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
      return { success: false };
    }
  }
};

export default servicioAutenticacion;
