import { useState, useEffect, useCallback, useMemo } from 'react';
import servicioPartidos from '../servicios/servicioPartidos';
import servicioLigas from '../servicios/servicioLigas';
import servicioCore from '../servicios/servicioCore';
import { useAuth } from '../contextos/ContextoAutenticacion';

export const usePartidos = () => {
  const { user } = useAuth();
  const POR_PAGINA = 10;
  const [partidos, setPartidos] = useState([]);
  const [selecciones, setSelecciones] = useState([]);
  const [ligas, setLigas] = useState([]);
  const [sedes, setSedes] = useState([]);
  const [ligaSeleccionada, setLigaSeleccionada] = useState('');
  const [estadoSeleccionado, setEstadoSeleccionado] = useState('');
  const [pagina, setPagina] = useState(1);
  const [totalRegistros, setTotalRegistros] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  const cargarPartidos = useCallback(async () => {
    try {
      setLoading(true);
      const result = await servicioPartidos.getPartidos(ligaSeleccionada, estadoSeleccionado, pagina, POR_PAGINA, searchTerm);

      if (result.success) {
        setPartidos(result.data.results ?? []);
        setTotalRegistros(result.data.count ?? 0);
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
  }, [ligaSeleccionada, estadoSeleccionado, pagina, searchTerm]);

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

  const cargarLigas = useCallback(async () => {
    try {
      const result = await servicioLigas.getLigas();
      if (result.success) {
        setLigas(result.data);
      }
    } catch (error) {
      console.error('Error al cargar ligas:', error);
    }
  }, []);

  const cargarSedes = useCallback(async () => {
    try {
      const result = await servicioCore.getSedes();
      if (result.success) {
        setSedes(result.data);
      }
    } catch (error) {
      console.error('Error al cargar sedes:', error);
    }
  }, []);

  useEffect(() => {
    cargarPartidos();
  }, [cargarPartidos]);

  useEffect(() => {
    cargarSelecciones();
    cargarLigas();
    cargarSedes();
  }, [cargarSelecciones, cargarLigas, cargarSedes]);

  // Resetear a página 1 cuando cambian filtros o búsqueda
  useEffect(() => {
    setPagina(1);
  }, [ligaSeleccionada, estadoSeleccionado, searchTerm]);

  const createPartido = async (partidoData) => {
    try {
      const result = await servicioPartidos.createPartido(partidoData);

      if (result.success) {
        await cargarPartidos();
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
        await cargarPartidos();
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
        await cargarPartidos();
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
        await cargarPartidos();
        return { success: true };
      } else {
        return { success: false, error: result.error || 'Error al actualizar resultado' };
      }
    } catch (err) {
      console.error('Error al actualizar resultado:', err);
      return { success: false, error: 'Error de conexión' };
    }
  };

  const ligasAdministradas = useMemo(() => {
    if (!user) return [];
    return ligas.filter(liga => liga.fk_administrador === user.id_usuario);
  }, [ligas, user]);

  const ligasAdministradasIds = useMemo(() => {
    const ids = new Set(ligasAdministradas.map(l => l.id_liga));
    // Incluir ligas públicas sin administrador (ej. liga mundial)
    ligas.forEach(liga => {
      if (liga.es_publica && (liga.fk_administrador === null || liga.fk_administrador === undefined)) {
        ids.add(Number(liga.id_liga));
      }
    });
    return ids;
  }, [ligasAdministradas, ligas]);

  const puedeGestionarLiga = useCallback(
    (ligaId) => {
      if (!ligaId) return false;
      return ligasAdministradasIds.has(Number(ligaId));
    },
    [ligasAdministradasIds]
  );

  const puedeGestionarLigaSeleccionada = useMemo(() => {
    if (!ligaSeleccionada) return false;
    return puedeGestionarLiga(ligaSeleccionada);
  }, [ligaSeleccionada, puedeGestionarLiga]);

  const filteredPartidos = partidos;

  return {
    partidos,
    selecciones,
    ligas,
    sedes,
    ligasAdministradas,
    puedeGestionarLiga,
    puedeGestionarLigaSeleccionada,
    ligaSeleccionada,
    setLigaSeleccionada,
    estadoSeleccionado,
    setEstadoSeleccionado,
    pagina,
    setPagina,
    totalRegistros,
    POR_PAGINA,
    loading,
    error,
    searchTerm,
    setSearchTerm,
    filteredPartidos,
    cargarPartidos,
    cargarSelecciones,
    cargarLigas,
    cargarSedes,
    createPartido,
    updatePartido,
    deletePartido,
    actualizarResultado
  };
};

export default usePartidos;
