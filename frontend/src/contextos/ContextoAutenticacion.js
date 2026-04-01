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
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  }, []);

  // Verificar autenticación al cargar
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          const response = await axios.get('http://localhost:8000/api/auth/check/');
          if (response.data.is_authenticated) {
            setUser(response.data.user);
            setIsAuthenticated(true);
          } else {
            localStorage.removeItem('token');
            localStorage.removeItem('refreshToken');
            delete axios.defaults.headers.common['Authorization'];
          }
        }
      } catch (error) {
        console.error('Error verificando autenticación:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        delete axios.defaults.headers.common['Authorization'];
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (email, password) => {
    try {
      const response = await axios.post('http://localhost:8000/api/auth/login/', {
        email,
        password
      });

      // Obtener tokens JWT
      const tokenResponse = await axios.post('http://localhost:8000/api/token/', {
        email,
        password
      });

      const { access, refresh } = tokenResponse.data;
      
      // Guardar tokens
      localStorage.setItem('token', access);
      localStorage.setItem('refreshToken', refresh);
      
      // Configurar axios para incluir token
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      setUser(response.data.user);
      setIsAuthenticated(true);
      
      return { success: true, user: response.data.user };
    } catch (error) {
      console.error('Error de login:', error);
      const errorMessage = error.response?.data?.non_field_errors?.[0] || 
                          error.response?.data?.detail || 
                          'Error al iniciar sesión';
      return { success: false, error: errorMessage };
    }
  };

  const register = async (userData) => {
    try {
      console.log('Enviando datos de registro:', userData);
      const response = await axios.post('http://localhost:8000/api/auth/register/', userData);
      console.log('Respuesta del servidor:', response.data);
      
      // Obtener tokens después del registro
      const tokenResponse = await axios.post('http://localhost:8000/api/token/', {
        email: userData.email,
        password: userData.password
      });

      const { access, refresh } = tokenResponse.data;
      
      // Guardar tokens
      localStorage.setItem('token', access);
      localStorage.setItem('refreshToken', refresh);
      
      // Configurar axios para incluir token
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      setUser(response.data.user);
      setIsAuthenticated(true);
      
      return { success: true, user: response.data.user };
    } catch (error) {
      console.error('Error de registro:', error);
      console.error('Datos del error:', error.response?.data);
      console.error('Status:', error.response?.status);
      
      // Mostrar errores más detallados
      let errorMessage = 'Error al registrar usuario';
      
      if (error.response?.data) {
        const errorData = error.response.data;
        
        // Si hay errores de campo específicos
        if (typeof errorData === 'object') {
          const errorMessages = [];
          
          // Revisar cada campo en busca de errores
          Object.keys(errorData).forEach(field => {
            if (Array.isArray(errorData[field])) {
              errorMessages.push(`${field}: ${errorData[field][0]}`);
            } else if (typeof errorData[field] === 'string') {
              errorMessages.push(`${field}: ${errorData[field]}`);
            }
          });
          
          if (errorMessages.length > 0) {
            errorMessage = errorMessages.join(', ');
          }
        } else if (errorData.detail) {
          errorMessage = errorData.detail;
        } else if (errorData.non_field_errors && errorData.non_field_errors[0]) {
          errorMessage = errorData.non_field_errors[0];
        }
      }
      
      return { success: false, error: errorMessage };
    }
  };

  const logout = async () => {
    try {
      await axios.post('http://localhost:8000/api/auth/logout/');
    } catch (error) {
      console.error('Error de logout:', error);
    } finally {
      // Limpiar tokens y estado
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
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
