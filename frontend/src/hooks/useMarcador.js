import { useState, useEffect, useCallback } from 'react';
import servicioMarcador from '../servicios/servicioMarcador';

export const useMarcador = () => {
  const [partidosEnVivo, setPartidosEnVivo] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [healthStatus, setHealthStatus] = useState(null);

  // Verificar estado del microservicio
  const checkHealth = useCallback(async () => {
    const result = await servicioMarcador.healthCheck();
    setHealthStatus(result);
    return result;
  }, []);

  // Obtener partidos en vivo
  const cargarPartidosEnVivo = useCallback(async () => {
    setLoading(true);
    setError(null);
    const result = await servicioMarcador.getPartidosEnVivo();
    if (result.success) {
      setPartidosEnVivo(result.data);
    } else {
      setError(result.error);
    }
    setLoading(false);
  }, []);

  // Actualizar marcador de un partido (optimistic update)
  const actualizarMarcador = useCallback(async (idPartido, golLocal, golVisitante, estado, faltasLocal, faltasVisitante) => {
    // Optimistic: actualizar UI inmediatamente
    setPartidosEnVivo(prev => prev.map(p => {
      if (p.id_partido !== idPartido) return p;
      return {
        ...p,
        gol_local: golLocal !== undefined ? golLocal : p.gol_local,
        gol_visitante: golVisitante !== undefined ? golVisitante : p.gol_visitante,
        faltas_local: faltasLocal !== undefined ? faltasLocal : p.faltas_local,
        faltas_visitante: faltasVisitante !== undefined ? faltasVisitante : p.faltas_visitante,
        estado: estado !== undefined ? estado : p.estado,
      };
    }));

    const result = await servicioMarcador.actualizarMarcador(
      idPartido,
      golLocal,
      golVisitante,
      estado,
      null,
      null,
      faltasLocal,
      faltasVisitante
    );
    if (result.success && result.data) {
      // Sincronizar con respuesta del servidor
      setPartidosEnVivo(prev => prev.map(p => p.id_partido === idPartido ? result.data : p));
    } else if (!result.success) {
      // Revertir si falló
      cargarPartidosEnVivo();
    }
    return result;
  }, [cargarPartidosEnVivo]);

  // Controlar partido (iniciar, pausar, cambiar tiempo, etc.) – optimistic update
  const controlarPartido = useCallback(async (idPartido, controlData) => {
    // Optimistic: actualizar UI inmediatamente
    setPartidosEnVivo(prev => prev.map(p => {
      if (p.id_partido !== idPartido) return p;
      return { ...p, ...controlData };
    }));

    const result = await servicioMarcador.controlarPartido(idPartido, controlData);
    if (result.success && result.data) {
      // Sincronizar con respuesta del servidor
      setPartidosEnVivo(prev => prev.map(p => p.id_partido === idPartido ? result.data : p));
    } else if (!result.success) {
      // Revertir si falló
      cargarPartidosEnVivo();
    }
    return result;
  }, [cargarPartidosEnVivo]);

  useEffect(() => {
    checkHealth();
  }, [checkHealth]);

  return {
    partidosEnVivo,
    loading,
    error,
    healthStatus,
    cargarPartidosEnVivo,
    actualizarMarcador,
    controlarPartido,
    checkHealth,
  };
};
