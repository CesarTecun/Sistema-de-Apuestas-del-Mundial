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

  // Actualizar marcador de un partido
  const actualizarMarcador = useCallback(async (idPartido, golLocal, golVisitante, estado, faltasLocal, faltasVisitante) => {
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
    if (result.success) {
      // Recargar partidos en vivo después de actualizar
      await cargarPartidosEnVivo();
    }
    return result;
  }, [cargarPartidosEnVivo]);

  // Controlar partido (iniciar, pausar, cambiar tiempo, etc.)
  const controlarPartido = useCallback(async (idPartido, controlData) => {
    const result = await servicioMarcador.controlarPartido(idPartido, controlData);
    if (result.success) {
      await cargarPartidosEnVivo();
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
