import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const ContextoAutenticacion = createContext();

export const useAuth = () => {
  const context = useContext(ContextoAutenticacion);
  if (!context) {
    // En lugar de lanzar un error, devolver un contexto seguro
    console.warn('useAuth debe usarse dentro de un ProveedorAutenticacion, devolviendo valores por defecto');
    return {
      user: null,
      isAuthenticated: false,
      loading: false,
      login: async () => ({ success: false, error: 'Contexto no disponible' }),
      register: async () => ({ success: false, error: 'Contexto no disponible' }),
      logout: async () => {}
    };
  }
  return context;
};

export const ProveedorAutenticacion = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Configurar axios para incluir token en todas las peticiones
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  }, []);

  // Verificar autenticación al cargar
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          const response = await axios.get('http://localhost:8000/api/auth/check/');
          if (response.data.is_authenticated) {
            setUser(response.data.user);
            setIsAuthenticated(true);
          } else {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            delete axios.defaults.headers.common['Authorization'];
          }
        }
      } catch (error) {
        console.error('Error verificando autenticación:', error);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        delete axios.defaults.headers.common['Authorization'];
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (email, password) => {
    try {
      // Paso 1: Login con el endpoint del backend (autenticación Django)
      const loginResponse = await axios.post('http://localhost:8000/api/auth/login/', {
        email,
        password
      });

      const user = loginResponse.data.user;

      // Paso 2: Obtener tokens JWT
      const tokenResponse = await axios.post('http://localhost:8000/api/token/', {
        email,
        password
      });

      const { access, refresh } = tokenResponse.data;
      
      // Guardar tokens con nombres consistentes
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      
      // Configurar axios para incluir token
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      setUser(user);
      setIsAuthenticated(true);
      
      return { success: true, user };
    } catch (error) {
      console.error('Error de login:', error);
      
      // Si el error es del login del backend
      if (error.response?.status === 400 && error.response?.data?.non_field_errors) {
        const errorMessage = error.response.data.non_field_errors[0];
        return { success: false, error: errorMessage };
      }
      
      // Si el error es de los tokens JWT
      if (error.response?.status === 401) {
        return { success: false, error: 'Credenciales incorrectas' };
      }
      
      const errorMessage = error.response?.data?.detail || 
                          error.response?.data?.message ||
                          'Error al iniciar sesión';
      return { success: false, error: errorMessage };
    }
  };

  const register = async (userData) => {
    try {
      console.log('Enviando datos de registro:', userData);
      
      // Paso 1: Registrar usuario
      const registerResponse = await axios.post('http://localhost:8000/api/auth/register/', userData);
      console.log('Respuesta del servidor:', registerResponse.data);
      
      const user = registerResponse.data.user;
      
      // Paso 2: Obtener tokens JWT automáticamente
      const tokenResponse = await axios.post('http://localhost:8000/api/token/', {
        email: userData.email,
        password: userData.password
      });

      const { access, refresh } = tokenResponse.data;
      
      // Guardar tokens con nombres consistentes
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      
      // Configurar axios para incluir token
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      setUser(user);
      setIsAuthenticated(true);
      
      return { success: true, user };
    } catch (error) {
      console.error('Error de registro:', error);
      console.error('Datos del error:', error.response?.data);
      console.error('Status:', error.response?.status);
      
      const errorMessage = error.response?.data?.email?.[0] || 
                          error.response?.data?.password?.[0] ||
                          error.response?.data?.password2?.[0] ||
                          error.response?.data?.non_field_errors?.[0] || 
                          error.response?.data?.detail || 
                          error.response?.data?.message ||
                          'Error al registrarse';
      return { success: false, error: errorMessage };
    }
  };

  const logout = async () => {
    try {
      await axios.post('http://localhost:8000/api/auth/logout/');
    } catch (error) {
      console.error('Error de logout:', error);
    } finally {
      // Limpiar tokens y estado con nombres consistentes
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      delete axios.defaults.headers.common['Authorization'];
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    register,
    logout
  };

  return (
    <ContextoAutenticacion.Provider value={value}>
      {children}
    </ContextoAutenticacion.Provider>
  );
};
