import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import { useMarcador } from '../../hooks/useMarcador';
import servicioPartidos from '../../servicios/servicioPartidos';
import servicioMarcador from '../../servicios/servicioMarcador';
import TopBar from '../Ligas/componentes/TopBar';
import '../../estilos/componentes/modals.css';
import './estilos/MarcadorPage.css';

const Cronometro = ({ partido, controlarPartido }) => {
  const [minuto, setMinuto] = useState(partido.minuto_actual || 0);
  const [periodo, setPeriodo] = useState(partido.periodo_actual || '1T');
  const [tiempoExtra, setTiempoExtra] = useState(partido.tiempo_extra_periodo || 0);
  const [pausado, setPausado] = useState(partido.partido_pausado || false);
  const [loadedFromStorage, setLoadedFromStorage] = useState(false);
  const [minutoInicioSegundoTiempo, setMinutoInicioSegundoTiempo] = useState(null);

  // Clave para localStorage
  const storageKey = `cronometro_${partido.id_partido}`;

  // Cargar estado desde localStorage al montar
  useEffect(() => {
    try {
      const saved = localStorage.getItem(storageKey);
      if (saved) {
        const data = JSON.parse(saved);
        // Solo usar datos guardados si el partido sigue iniciado
        if (partido.partido_iniciado && partido.estado !== 'finalizado') {
          setMinuto(data.minuto || partido.minuto_actual || 0);
          setPeriodo(data.periodo || partido.periodo_actual || '1T');
          setTiempoExtra(data.tiempoExtra || partido.tiempo_extra_periodo || 0);
          setPausado(data.pausado || partido.partido_pausado || false);
          setLoadedFromStorage(true);
        } else {
          setLoadedFromStorage(true);
        }
      } else {
        setLoadedFromStorage(true);
      }
    } catch (e) {
      console.error('[Cronometro] Error al cargar cronómetro desde localStorage:', e);
      setLoadedFromStorage(true);
    }
  }, [partido.id_partido, partido.partido_iniciado, partido.estado, storageKey]);

  // Guardar estado en localStorage cuando cambie (solo después de cargar)
  useEffect(() => {
    if (!loadedFromStorage) return; // No guardar hasta que se cargue desde localStorage
    
    try {
      const data = { minuto, periodo, tiempoExtra, pausado };
      localStorage.setItem(storageKey, JSON.stringify(data));
    } catch (e) {
      console.error('Error al guardar cronómetro en localStorage:', e);
    }
  }, [minuto, periodo, tiempoExtra, pausado, storageKey, loadedFromStorage]);

  // Limpiar localStorage cuando el partido se finaliza
  useEffect(() => {
    if (partido.estado === 'finalizado' || !partido.partido_iniciado) {
      try {
        localStorage.removeItem(storageKey);
      } catch (e) {
        console.error('Error al limpiar localStorage:', e);
      }
    }
  }, [partido.estado, partido.partido_iniciado, storageKey]);

  // Sincronizar estado local con cambios del partido (periodo, tiempo extra, etc.)
  useEffect(() => {
    if (loadedFromStorage) {
      const periodoAnterior = periodo;
      const nuevoPeriodo = partido.periodo_actual || '1T';
      setPeriodo(nuevoPeriodo);
      setTiempoExtra(partido.tiempo_extra_periodo || 0);
      setPausado(partido.partido_pausado || false);

      // Si cambió de 1T a 2T, guardar el minuto de inicio del segundo tiempo
      if (periodoAnterior === '1T' && nuevoPeriodo === '2T') {
        setMinutoInicioSegundoTiempo(minuto);
      }
    }
  }, [partido.periodo_actual, partido.tiempo_extra_periodo, partido.partido_pausado, loadedFromStorage, periodo, minuto]);

  useEffect(() => {
    if (!partido.partido_iniciado || partido.partido_pausado || partido.estado === 'finalizado') {
      return;
    }

    const interval = setInterval(() => {
      setMinuto(prev => {
        // Calcular el límite del periodo considerando el tiempo extra
        let limiteMinuto;
        if (periodo === '1T') {
          limiteMinuto = 44 + tiempoExtra;
        } else if (periodo === '2T') {
          // Para el segundo tiempo, el límite es el minuto de inicio + 44 + tiempo extra
          limiteMinuto = (minutoInicioSegundoTiempo || 0) + 44 + tiempoExtra;
        } else {
          limiteMinuto = 44 + tiempoExtra;
        }

        // Si llega al límite y está en 1T, pausar y cambiar a 2T
        if (prev === limiteMinuto && periodo === '1T') {
          // Pausar automáticamente al final del primer tiempo (usar setTimeout para evitar warning)
          setTimeout(() => {
            controlarPartido(partido.id_partido, { partido_pausado: true, periodo_actual: '2T' });
          }, 0);
          setPeriodo('2T');
          // No reiniciar a 0, mantener el minuto actual
          return prev;
        }
        // Si llega al límite y está en 2T, solo pausar (no finalizar)
        if (prev === limiteMinuto && periodo === '2T') {
          // Pausar automáticamente al final del segundo tiempo (usar setTimeout para evitar warning)
          setTimeout(() => {
            controlarPartido(partido.id_partido, { partido_pausado: true });
          }, 0);
          return prev;
        }
        return prev + 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [partido.partido_iniciado, partido.partido_pausado, partido.estado, periodo, tiempoExtra, controlarPartido, minutoInicioSegundoTiempo]);

  const formatoTiempo = () => {
    if (tiempoExtra > 0) {
      return `${minuto}+${tiempoExtra}`;
    }
    return minuto;
  };

  return (
    <div className="cronometro-container">
      <div className="cronometro-time">
        {formatoTiempo()}' {periodo}
      </div>
      {!partido.partido_iniciado && partido.estado !== 'finalizado' && (
        <div className="cronometro-status not-started">No iniciado</div>
      )}
    </div>
  );
};

const MarcadorPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const {
    partidosEnVivo,
    loading,
    error,
    cargarPartidosEnVivo,
    actualizarMarcador,
    controlarPartido,
  } = useMarcador();

  const [selectedPartidoId, setSelectedPartidoId] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);
  const [actionError, setActionError] = useState(null);
  const [selecciones, setSelecciones] = useState([]);
  const [partidoIndividual, setPartidoIndividual] = useState(null);
  const [partidoNoDisponible, setPartidoNoDisponible] = useState(false);

  useEffect(() => {
    // Si viene un partidoId desde la navegación, seleccionarlo
    if (location.state?.partidoId) {
      setSelectedPartidoId(location.state.partidoId);
    }
  }, [location.state]);

  useEffect(() => {
    // Cargar selecciones
    servicioPartidos.getSelecciones().then(res => {
      if (res.success) {
        setSelecciones(res.data);
      }
    });
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate('/home');
  };

  useEffect(() => {
    cargarPartidosEnVivo();
    const interval = setInterval(() => {
      cargarPartidosEnVivo();
    }, 10000);
    return () => clearInterval(interval);
  }, [cargarPartidosEnVivo]);

  // Verificar si el partido seleccionado está disponible
  useEffect(() => {
    if (selectedPartidoId && partidosEnVivo.length > 0) {
      const partidoExiste = partidosEnVivo.some(p => p.id_partido === Number(selectedPartidoId));
      if (!partidoExiste) {
        setPartidoIndividual(null);
        setPartidoNoDisponible(true);
      } else {
        setPartidoIndividual(null);
        setPartidoNoDisponible(false);
      }
    }
  }, [selectedPartidoId, partidosEnVivo]);

  const getSeleccionNombre = (id) => {
    const seleccion = selecciones.find((s) => s.id_seleccion === id);
    return seleccion ? seleccion.pais : `Equipo ${id}`;
  };

  const getSeleccionBandera = (id) => {
    const seleccion = selecciones.find((s) => s.id_seleccion === id);
    return seleccion ? seleccion.bandera : null;
  };

  const handleActualizarMarcador = async (idPartido, golLocal, golVisitante, faltasLocal, faltasVisitante) => {
    setActionLoading(true);
    setActionError(null);
    const result = await actualizarMarcador(idPartido, golLocal, golVisitante, 'en_juego', faltasLocal, faltasVisitante);
    setActionLoading(false);
    if (!result.success) {
      setActionError(result.error || 'Error al actualizar marcador');
    }
  };

  const handleIniciarPartido = async (idPartido) => {
    setActionLoading(true);
    setActionError(null);
    const result = await controlarPartido(idPartido, { partido_iniciado: true });
    setActionLoading(false);
    if (!result.success) {
      setActionError(result.error || 'Error al iniciar partido');
    }
  };

  const handlePausarPartido = async (idPartido, pausado) => {
    setActionLoading(true);
    setActionError(null);
    const result = await controlarPartido(idPartido, { partido_pausado: pausado });
    setActionLoading(false);
    if (!result.success) {
      setActionError(result.error || 'Error al pausar/reanudar partido');
    }
  };

  const handleCambiarPeriodo = async (idPartido, nuevoPeriodo) => {
    setActionLoading(true);
    setActionError(null);
    const result = await controlarPartido(idPartido, { periodo_actual: nuevoPeriodo });
    setActionLoading(false);
    if (!result.success) {
      setActionError(result.error || 'Error al cambiar período');
    }
  };

  const handleAgregarTiempoExtra = async (idPartido, minutos) => {
    setActionLoading(true);
    setActionError(null);
    const result = await controlarPartido(idPartido, { tiempo_extra_periodo: minutos });
    setActionLoading(false);
    if (!result.success) {
      setActionError(result.error || 'Error al agregar tiempo extra');
    }
  };

  const handleFinalizarPartido = async (idPartido) => {
    setActionLoading(true);
    setActionError(null);
    const result = await controlarPartido(idPartido, { estado: 'finalizado' });
    setActionLoading(false);
    if (result.success) {
      navigate('/partidos');
    } else {
      setActionError(result.error || 'Error al finalizar partido');
    }
  };

  if (loading && partidosEnVivo.length === 0) {
    return (
      <div className="marcador-container">
        <div className="marcador-background">
          <div className="marcador-wrapper">
            <div className="loading-container">
              <div className="loading-spinner"></div>
              <p>Cargando marcador...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="marcador-container">
      <div className="marcador-background">
        <div className="marcador-wrapper">
          <TopBar user={user} onLogout={handleLogout} />

          <div className="marcador-content">
            {/* Header del Marcador */}
            <div className="marcador-header">
              <h1>Marcador en Vivo</h1>
              <button
                onClick={() => cargarPartidosEnVivo()}
                className="refresh-button"
              >
                Recargar
              </button>
            </div>

            {/* Error */}
            {error && (
              <div className="error-message">
                <p>{error}</p>
              </div>
            )}
            {actionError && (
              <div className="error-message">
                <p>{actionError}</p>
                <button onClick={() => setActionError(null)} className="dismiss-error">×</button>
              </div>
            )}

            {/* Lista de partidos en vivo */}
            {!selectedPartidoId ? (
              <div className="empty-state">
                <div className="empty-icon">
                  <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="2" y1="12" x2="22" y2="12"></line>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                  </svg>
                </div>
                <h3>No hay partido seleccionado</h3>
                <p>Selecciona un partido desde la página de partidos para ver su marcador.</p>
              </div>
            ) : partidoNoDisponible ? (
              <div className="empty-state">
                <div className="empty-icon">
                  <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="15" y1="9" x2="9" y2="15"></line>
                    <line x1="9" y1="9" x2="15" y2="15"></line>
                  </svg>
                </div>
                <h3>Partido no disponible</h3>
                <p>Este partido no está disponible en el sistema de marcador. Solo los partidos en vivo pueden ser gestionados.</p>
                <button
                  onClick={() => navigate('/partidos')}
                  className="control-button control-button-blue"
                  style={{ marginTop: '16px' }}
                >
                  Volver a Partidos
                </button>
              </div>
            ) : (
              (() => {
                const partidosAMostrar = partidoIndividual
                  ? [partidoIndividual]
                  : partidosEnVivo.filter(p => p.id_partido === Number(selectedPartidoId));
                return partidosAMostrar.map((partido) => (
                  <div key={partido.id_partido} className="partido-card">
                  {/* Encabezado del partido */}
                  <div className="partido-header">
                    <div className="partido-teams">
                      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        {getSeleccionBandera(partido.equipo_local) && (
                          <img
                            src={getSeleccionBandera(partido.equipo_local)}
                            alt=""
                            style={{ width: '40px', height: '26px', borderRadius: '3px', objectFit: 'cover' }}
                          />
                        )}
                        <h3>
                          {getSeleccionNombre(partido.equipo_local)} vs {getSeleccionNombre(partido.equipo_visitante)}
                        </h3>
                        {getSeleccionBandera(partido.equipo_visitante) && (
                          <img
                            src={getSeleccionBandera(partido.equipo_visitante)}
                            alt=""
                            style={{ width: '40px', height: '26px', borderRadius: '3px', objectFit: 'cover' }}
                          />
                        )}
                      </div>
                      <p>Estado: {partido.estado}</p>
                    </div>
                    <div className="partido-score">
                      {partido.gol_local} - {partido.gol_visitante}
                    </div>
                  </div>

                  {/* Resultado final si está finalizado */}
                  {partido.estado === 'finalizado' && (
                    <div className="resultado-final">
                      <h2>Resultado Final</h2>
                      <div className="resultado-marcador">
                        <div className="resultado-equipo">
                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            {getSeleccionBandera(partido.equipo_local) && (
                              <img
                                src={getSeleccionBandera(partido.equipo_local)}
                                alt=""
                                style={{ width: '32px', height: '20px', borderRadius: '2px', objectFit: 'cover' }}
                              />
                            )}
                            <span className="equipo-nombre">{getSeleccionNombre(partido.equipo_local)}</span>
                          </div>
                          <span className="equipo-goles">{partido.gol_local}</span>
                        </div>
                        <div className="resultado-separador">-</div>
                        <div className="resultado-equipo">
                          <span className="equipo-goles">{partido.gol_visitante}</span>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <span className="equipo-nombre">{getSeleccionNombre(partido.equipo_visitante)}</span>
                            {getSeleccionBandera(partido.equipo_visitante) && (
                              <img
                                src={getSeleccionBandera(partido.equipo_visitante)}
                                alt=""
                                style={{ width: '32px', height: '20px', borderRadius: '2px', objectFit: 'cover' }}
                              />
                            )}
                          </div>
                        </div>
                      </div>
                      {partido.resultado && (
                        <p className="resultado-texto">{partido.resultado}</p>
                      )}
                    </div>
                  )}

                  {/* Solo mostrar controles si NO está finalizado */}
                  {partido.estado !== 'finalizado' && (
                    <>
                      {/* Cronómetro */}
                      <Cronometro
                        partido={partido}
                        controlarPartido={controlarPartido}
                      />

                      {/* Controles de marcador */}
                      <div className="controls-section">
                        <h4>Goles</h4>
                        <div className="controls-grid">
                          <button
                            onClick={() => handleActualizarMarcador(partido.id_partido, partido.gol_local + 1, partido.gol_visitante, partido.faltas_local, partido.faltas_visitante)}
                            className="control-button control-button-green"
                            disabled={actionLoading}
                          >
                            +1 Local
                          </button>
                          <button
                            onClick={() => handleActualizarMarcador(partido.id_partido, partido.gol_local, partido.gol_visitante + 1, partido.faltas_local, partido.faltas_visitante)}
                            className="control-button control-button-green"
                            disabled={actionLoading}
                          >
                            +1 Visitante
                          </button>
                        </div>
                      </div>

                      {/* Controles de faltas */}
                      <div className="controls-section">
                        <h4>Faltas</h4>
                        <div className="faltas-container">
                          <div className="falta-control">
                            <span>Local: {partido.faltas_local || 0}</span>
                            <button
                              onClick={() => handleActualizarMarcador(partido.id_partido, partido.gol_local, partido.gol_visitante, (partido.faltas_local || 0) + 1, partido.faltas_visitante)}
                              className="control-button control-button-yellow"
                              disabled={actionLoading}
                            >
                              +1
                            </button>
                          </div>
                          <div className="falta-control">
                            <span>Visitante: {partido.faltas_visitante || 0}</span>
                            <button
                              onClick={() => handleActualizarMarcador(partido.id_partido, partido.gol_local, partido.gol_visitante, partido.faltas_local, (partido.faltas_visitante || 0) + 1)}
                              className="control-button control-button-yellow"
                              disabled={actionLoading}
                            >
                              +1
                            </button>
                          </div>
                        </div>
                      </div>

                      {/* Control del partido */}
                      <div className="controls-section">
                        <h4>Control del Partido</h4>
                        <div className="controls-grid">
                          {!partido.partido_iniciado && (
                            <button
                              onClick={() => handleIniciarPartido(partido.id_partido)}
                              className="control-button control-button-blue"
                              disabled={actionLoading}
                            >
                              Iniciar
                            </button>
                          )}
                          {partido.partido_iniciado && (
                            <>
                              <button
                                onClick={() => handlePausarPartido(partido.id_partido, !partido.partido_pausado)}
                                className="control-button control-button-orange"
                                disabled={actionLoading || partido.estado === 'finalizado'}
                              >
                                {partido.partido_pausado ? 'Reanudar' : 'Pausar'}
                              </button>
                              <button
                                onClick={() => handleCambiarPeriodo(partido.id_partido, partido.periodo_actual === '1T' ? '2T' : '1T')}
                                className="control-button control-button-purple"
                                disabled={actionLoading || partido.estado === 'finalizado'}
                              >
                                Cambiar período
                              </button>
                              <button
                                onClick={() => handleAgregarTiempoExtra(partido.id_partido, (partido.tiempo_extra_periodo || 0) + 3)}
                                className="control-button control-button-indigo"
                                disabled={actionLoading || partido.estado === 'finalizado'}
                              >
                                +3 min extra
                              </button>
                              <button
                                onClick={() => handleFinalizarPartido(partido.id_partido)}
                                className="control-button control-button-red"
                                disabled={actionLoading || partido.estado === 'finalizado'}
                              >
                                Finalizar
                              </button>
                            </>
                          )}
                        </div>
                      </div>

                      {/* Información del partido */}
                      <div className="partido-info">
                        <div className="partido-info-grid">
                          <div>Período: {partido.periodo_actual || '1T'}</div>
                          <div>Tiempo extra: {partido.tiempo_extra_periodo || 0} min</div>
                          <div>Iniciado: {partido.partido_iniciado ? 'Sí' : 'No'}</div>
                          <div>Pausado: {partido.partido_pausado ? 'Sí' : 'No'}</div>
                        </div>
                      </div>
                    </>
                  )}
                </div>
              ))
              })()
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarcadorPage;
