import { useState, useEffect, useCallback } from 'react';
import servicioPartidos from '../servicios/servicioPartidos';

export const usePartidos = () => {
  const [partidos, setPartidos] = useState([]);
  const [selecciones, setSelecciones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  const cargarPartidos = useCallback(async () => {
    try {
      setLoading(true);
      const result = await servicioPartidos.getPartidos();

      if (result.success) {
        setPartidos(result.data);
        setError('');
      } else {
        setError(result.error || 'Error al cargar los partidos');
      }
    } catch (error) {
      console.error('Error al cargar partidos:', error);
      setError('Error al cargar los partidos. Verifica que el backend esté corriendo.');
    } finally {
      setLoading(false);
    }
  }, []);

  const cargarSelecciones = useCallback(async () => {
    try {
      const result = await servicioPartidos.getSelecciones();

      if (result.success) {
        setSelecciones(result.data);
      }
    } catch (error) {
      console.error('Error al cargar selecciones:', error);
    }
  }, []);

  useEffect(() => {
    cargarPartidos();
    cargarSelecciones();
  }, [cargarPartidos, cargarSelecciones]);

  const createPartido = async (partidoData) => {
    try {
      const result = await servicioPartidos.createPartido(partidoData);

      if (result.success) {
        setPartidos([...partidos, result.data]);
        return { success: true };
      } else {
        return { success: false, error: result.error || 'Error al crear partido' };
      }
    } catch (err) {
      console.error('Error al crear partido:', err);
      return { success: false, error: 'Error de conexión' };
    }
  };

  const updatePartido = async (partidoId, partidoData) => {
    try {
      const result = await servicioPartidos.updatePartido(partidoId, partidoData);

      if (result.success) {
        setPartidos(partidos.map(partido => 
          partido.id_partido === result.data.id_partido ? result.data : partido
        ));
        return { success: true };
      } else {
        return { success: false, error: result.error || 'Error al actualizar partido' };
      }
    } catch (err) {
      console.error('Error al actualizar partido:', err);
      return { success: false, error: 'Error de conexión' };
    }
  };

  const deletePartido = async (partidoId) => {
    try {
      const result = await servicioPartidos.deletePartido(partidoId);

      if (result.success) {
        setPartidos(partidos.filter(partido => partido.id_partido !== partidoId));
        return { success: true };
      } else {
        return { success: false, error: result.error || 'Error al eliminar partido' };
      }
    } catch (err) {
      console.error('Error al eliminar partido:', err);
      return { success: false, error: 'Error de conexión' };
    }
  };

  const actualizarResultado = async (partidoId, golLocal, golVisitante, resultado) => {
    try {
      const result = await servicioPartidos.actualizarResultado(partidoId, golLocal, golVisitante, resultado);

      if (result.success) {
        setPartidos(partidos.map(partido => 
          partido.id_partido === result.data.id_partido ? result.data : partido
        ));
        return { success: true };
      } else {
        return { success: false, error: result.error || 'Error al actualizar resultado' };
      }
    } catch (err) {
      console.error('Error al actualizar resultado:', err);
      return { success: false, error: 'Error de conexión' };
    }
  };

  const filteredPartidos = partidos.filter(partido => {
    const searchLower = searchTerm.toLowerCase();
    // Buscar por IDs de equipos (que corresponden a selecciones)
    const equipoLocal = selecciones.find(s => s.id_seleccion === partido.equipo_local);
    const equipoVisitante = selecciones.find(s => s.id_seleccion === partido.equipo_visitante);
    
    const nombreLocal = equipoLocal?.pais?.toLowerCase() || '';
    const nombreVisitante = equipoVisitante?.pais?.toLowerCase() || '';
    
    return nombreLocal.includes(searchLower) || 
           nombreVisitante.includes(searchLower) ||
           partido.tipo_partido?.toLowerCase().includes(searchLower) ||
           partido.resultado?.toLowerCase().includes(searchLower);
  });

  return {
    partidos,
    selecciones,
    loading,
    error,
    searchTerm,
    setSearchTerm,
    filteredPartidos,
    cargarPartidos,
    cargarSelecciones,
    createPartido,
    updatePartido,
    deletePartido,
    actualizarResultado
  };
};

export default usePartidos;
