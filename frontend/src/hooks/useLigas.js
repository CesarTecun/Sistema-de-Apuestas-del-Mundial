import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../contextos/ContextoAutenticacion';
import { API_ENDPOINTS } from '../config/apiConfig';

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
      const response = await axios.get(API_ENDPOINTS.LIGAS);
      setLigas(response.data);
      setError('');
    } catch (error) {
      console.error('Error al cargar ligas:', error);
      if (error.response?.status === 401) {
        logout();
        navigate('/login');
        return;
      }
      setError('Error al cargar las ligas. Verifica que el backend esté corriendo.');
    } finally {
      setLoading(false);
    }
  }, [logout, navigate]);

  const createLiga = async (ligaData) => {
    try {
      const response = await axios.post(API_ENDPOINTS.LIGAS, ligaData);
      setLigas([...ligas, response.data]);
      return { success: true };
    } catch (err) {
      console.error('Error al crear liga:', err);
      if (err.response?.status === 401) {
        logout();
        navigate('/login');
        return { success: false, error: 'Sesión expirada' };
      }
      return { success: false, error: 'Error al crear liga' };
    }
  };

  const updateLiga = async (ligaId, ligaData) => {
    try {
      const response = await axios.put(`${API_ENDPOINTS.LIGAS}${ligaId}/`, ligaData);
      setLigas(ligas.map(liga => 
        liga.id_liga === response.data.id_liga ? response.data : liga
      ));
      return { success: true };
    } catch (err) {
      console.error('Error al actualizar liga:', err);
      if (err.response?.status === 401) {
        logout();
        navigate('/login');
        return { success: false, error: 'Sesión expirada' };
      }
      return { success: false, error: 'Error al actualizar liga' };
    }
  };

  const deleteLiga = async (ligaId) => {
    try {
      await axios.delete(`${API_ENDPOINTS.LIGAS}${ligaId}/`);
      setLigas(ligas.filter(liga => liga.id_liga !== ligaId));
      return { success: true };
    } catch (err) {
      console.error('Error al eliminar liga:', err);
      if (err.response?.status === 401) {
        logout();
        navigate('/login');
        return { success: false, error: 'Sesión expirada' };
      }
      return { success: false, error: 'Error al eliminar liga' };
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
