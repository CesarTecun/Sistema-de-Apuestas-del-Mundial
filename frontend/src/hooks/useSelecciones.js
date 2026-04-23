import { useState, useEffect, useCallback } from 'react';
import servicioSelecciones from '../servicios/servicioSelecciones';

export const useSelecciones = () => {
  const [selecciones, setSelecciones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  const cargarSelecciones = useCallback(async () => {
    try {
      setLoading(true);
      const result = await servicioSelecciones.getSelecciones();

      if (result.success) {
        setSelecciones(result.data);
        setError('');
      } else {
        setError(result.error || 'Error al cargar las selecciones');
      }
    } catch (error) {
      console.error('Error al cargar selecciones:', error);
      setError('Error al cargar las selecciones. Verifica que el backend esté corriendo.');
    } finally {
      setLoading(false);
    }
  }, []);

  const createSeleccion = async (seleccionData) => {
    try {
      const result = await servicioSelecciones.createSeleccion(seleccionData);

      if (result.success) {
        setSelecciones([...selecciones, result.data]);
        return { success: true };
      } else {
        return { success: false, error: result.error || 'Error al crear selección' };
      }
    } catch (err) {
      console.error('Error al crear selección:', err);
      return { success: false, error: 'Error de conexión' };
    }
  };

  const updateSeleccion = async (seleccionId, seleccionData) => {
    try {
      const result = await servicioSelecciones.updateSeleccion(seleccionId, seleccionData);

      if (result.success) {
        setSelecciones(selecciones.map(seleccion => 
          seleccion.id_seleccion === result.data.id_seleccion ? result.data : seleccion
        ));
        return { success: true };
      } else {
        return { success: false, error: result.error || 'Error al actualizar selección' };
      }
    } catch (err) {
      console.error('Error al actualizar selección:', err);
      return { success: false, error: 'Error de conexión' };
    }
  };

  const deleteSeleccion = async (seleccionId) => {
    try {
      const result = await servicioSelecciones.deleteSeleccion(seleccionId);

      if (result.success) {
        setSelecciones(selecciones.filter(seleccion => seleccion.id_seleccion !== seleccionId));
        return { success: true };
      } else {
        return { success: false, error: result.error || 'Error al eliminar selección' };
      }
    } catch (err) {
      console.error('Error al eliminar selección:', err);
      return { success: false, error: 'Error de conexión' };
    }
  };

  const filteredSelecciones = selecciones.filter(seleccion =>
    seleccion.pais.toLowerCase().includes(searchTerm.toLowerCase()) ||
    seleccion.bandera?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  useEffect(() => {
    cargarSelecciones();
  }, [cargarSelecciones]);

  return {
    selecciones,
    loading,
    error,
    searchTerm,
    setSearchTerm,
    filteredSelecciones,
    cargarSelecciones,
    createSeleccion,
    updateSeleccion,
    deleteSeleccion
  };
};

export default useSelecciones;
