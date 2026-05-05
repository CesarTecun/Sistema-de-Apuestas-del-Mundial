import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contextos/ContextoAutenticacion';
import { API_ENDPOINTS, getAuthHeaders } from '../config/apiConfig';

export const useLigas = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [ligas, setLigas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  const cargarLigas = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch(API_ENDPOINTS.LIGAS, {
        headers: getAuthHeaders()
      });
      
      if (!response.ok) {
        if (response.status === 401) {
          logout();
          navigate('/login');
          return;
        }
        if (response.status === 404) {
          throw new Error('Endpoint no encontrado. El servidor puede no estar corriendo.');
        }
        throw new Error(`Error HTTP: ${response.status}`);
      }
      
      const data = await response.json();
      setLigas(data);
      setError('');
    } catch (error) {
      console.error('Error al cargar ligas:', error);
      setError('Error al cargar las ligas. Verifica que el backend esté corriendo.');
    } finally {
      setLoading(false);
    }
  }, [logout, navigate]);

  const createLiga = async (ligaData) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/ligas/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(ligaData),
      });

      if (response.ok) {
        const nuevaLiga = await response.json();
        setLigas([...ligas, nuevaLiga]);
        return { success: true };
      } else {
        if (response.status === 401) {
          logout();
          navigate('/login');
          return { success: false, error: 'Sesión expirada' };
        }
        const errorData = await response.json();
        return { success: false, error: errorData.message || 'Error al crear liga' };
      }
    } catch (err) {
      console.error('Error al crear liga:', err);
      return { success: false, error: 'Error de conexión' };
    }
  };

  const updateLiga = async (ligaId, ligaData) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://localhost:8000/api/ligas/${ligaId}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(ligaData),
      });

      if (response.ok) {
        const ligaActualizada = await response.json();
        setLigas(ligas.map(liga => 
          liga.id_liga === ligaActualizada.id_liga ? ligaActualizada : liga
        ));
        return { success: true };
      } else {
        if (response.status === 401) {
          logout();
          navigate('/login');
          return { success: false, error: 'Sesión expirada' };
        }
        const errorData = await response.json();
        return { success: false, error: errorData.message || 'Error al actualizar liga' };
      }
    } catch (err) {
      console.error('Error al actualizar liga:', err);
      return { success: false, error: 'Error de conexión' };
    }
  };

  const deleteLiga = async (ligaId) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://localhost:8000/api/ligas/${ligaId}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        setLigas(ligas.filter(liga => liga.id_liga !== ligaId));
        return { success: true };
      } else {
        if (response.status === 401) {
          logout();
          navigate('/login');
          return { success: false, error: 'Sesión expirada' };
        }
        const errorData = await response.json();
        return { success: false, error: errorData.message || 'Error al eliminar liga' };
      }
    } catch (err) {
      console.error('Error al eliminar liga:', err);
      return { success: false, error: 'Error de conexión' };
    }
  };

  const filteredLigas = ligas.filter(liga =>
    liga.nombre_liga.toLowerCase().includes(searchTerm.toLowerCase()) ||
    liga.tipo_liga?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    liga.estado?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  useEffect(() => {
    cargarLigas();
  }, [cargarLigas]);

  return {
    ligas,
    loading,
    error,
    searchTerm,
    setSearchTerm,
    filteredLigas,
    cargarLigas,
    createLiga,
    updateLiga,
    deleteLiga
  };
};
