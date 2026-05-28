import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import servicioPartidos from '../../servicios/servicioPartidos';
import TopBar from '../../componentes/TopBar';
import './estilos/CalendarioPage.css';

const formatearFechaCorta = (fecha) => {
  return fecha.toLocaleDateString('es-ES', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
  });
};

const formatearFechaLarga = (fecha) => {
  return fecha.toLocaleDateString('es-ES', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
};

const formatearHora = (fechaStr) => {
  const fecha = new Date(fechaStr);
  return fecha.toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit',
  });
};

const getFechaKey = (fechaStr) => {
  // Usar componentes UTC para strings ISO del backend y evitar desfases de zona horaria
  const fecha = new Date(fechaStr);
  const year = fecha.getUTCFullYear();
  const month = String(fecha.getUTCMonth() + 1).padStart(2, '0');
  const day = String(fecha.getUTCDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

const getLocalDateKey = (fecha) => {
  const year = fecha.getFullYear();
  const month = String(fecha.getMonth() + 1).padStart(2, '0');
  const day = String(fecha.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

const CalendarioPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [partidos, setPartidos] = useState([]);
  const [selecciones, setSelecciones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [fechaSeleccionada, setFechaSeleccionada] = useState(new Date());
  const [refreshing, setRefreshing] = useState(false);

  const cargarDatos = useCallback(async () => {
    try {
      setLoading(true);
      const [partidosRes, seleccionesRes] = await Promise.all([
        servicioPartidos.getPartidos(undefined, undefined, 1, 100),
        servicioPartidos.getSelecciones(),
      ]);

      if (partidosRes.success) {
        setPartidos(partidosRes.data.results ?? []);
      } else {
        setError(partidosRes.error || 'Error al cargar partidos');
      }

      if (seleccionesRes.success) {
        setSelecciones(seleccionesRes.data);
      }
    } catch (err) {
      console.error('Error al cargar calendario:', err);
      setError('Error al cargar el calendario');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    cargarDatos();
  }, [cargarDatos]);

  // Refrescar cada 30 segundos si hay partidos en vivo
  useEffect(() => {
    const hayEnVivo = partidos.some(
      (p) => p.estado_partido === 'en_juego'
    );
    if (!hayEnVivo) return;

    const interval = setInterval(() => {
      setRefreshing(true);
      servicioPartidos.getPartidos(undefined, undefined, 1, 100).then((res) => {
        if (res.success) setPartidos(res.data.results ?? []);
        setRefreshing(false);
      });
    }, 30000);

    return () => clearInterval(interval);
  }, [partidos]);

  const partidosPorFecha = useMemo(() => {
    const agrupados = {};
    partidos.forEach((partido) => {
      const key = getFechaKey(partido.horario);
      if (!agrupados[key]) agrupados[key] = [];
      agrupados[key].push(partido);
    });
    // Ordenar cada grupo por hora
    Object.keys(agrupados).forEach((key) => {
      agrupados[key].sort(
        (a, b) => new Date(a.horario) - new Date(b.horario)
      );
    });
    return agrupados;
  }, [partidos]);

  const fechasDisponibles = useMemo(() => {
    return Object.keys(partidosPorFecha).sort();
  }, [partidosPorFecha]);

  const fechaKeyActual = useMemo(() => {
    return getLocalDateKey(fechaSeleccionada);
  }, [fechaSeleccionada]);

  const partidosDelDia = useMemo(() => {
    return partidosPorFecha[fechaKeyActual] || [];
  }, [partidosPorFecha, fechaKeyActual]);

  const navigateFecha = (direccion) => {
    const idx = fechasDisponibles.indexOf(fechaKeyActual);
    if (idx === -1) {
      // Si la fecha actual no tiene partidos, buscar la más cercana
      const futuras = fechasDisponibles.filter((f) => f >= fechaKeyActual);
      const pasadas = fechasDisponibles.filter((f) => f < fechaKeyActual);
      const target =
        direccion === 'next'
          ? futuras[0] || fechasDisponibles[0]
          : pasadas[pasadas.length - 1] || fechasDisponibles[fechasDisponibles.length - 1];
      if (target) setFechaSeleccionada(new Date(target + 'T00:00:00'));
      return;
    }

    const nuevoIdx =
      direccion === 'next'
        ? Math.min(idx + 1, fechasDisponibles.length - 1)
        : Math.max(idx - 1, 0);
    const nuevaFecha = fechasDisponibles[nuevoIdx];
    if (nuevaFecha) {
      setFechaSeleccionada(new Date(nuevaFecha + 'T00:00:00'));
    }
  };

  const getSeleccionNombre = (id) => {
    const seleccion = selecciones.find((s) => s.id_seleccion === id);
    return seleccion ? seleccion.pais : `Equipo ${id}`;
  };

  const getSeleccionBandera = (id) => {
    const seleccion = selecciones.find((s) => s.id_seleccion === id);
    return seleccion ? seleccion.bandera : null;
  };

  const getEstadoInfo = (partido) => {
    if (partido.estado_partido === 'finalizado' || partido.resultado) {
      return { clase: 'finalizado', texto: 'Finalizado', enVivo: false };
    }
    if (partido.estado_partido === 'en_juego') {
      return { clase: 'en-vivo', texto: 'En Vivo', enVivo: true };
    }
    const horario = new Date(partido.horario);
    const ahora = new Date();
    if (horario < ahora) {
      return { clase: 'en-vivo', texto: 'En Vivo', enVivo: true };
    }
    return { clase: 'pendiente', texto: 'Pendiente', enVivo: false };
  };

  const handleLogout = async () => {
    await logout();
    navigate('/home');
  };

  const handleIrMarcador = (partidoId) => {
    navigate('/marcador', { state: { partidoId } });
  };

  const fechaPickerValue = getLocalDateKey(fechaSeleccionada);

  const handleDateChange = (e) => {
    const val = e.target.value;
    if (val) setFechaSeleccionada(new Date(val + 'T00:00:00'));
  };

  const enVivoCount = partidosDelDia.filter(
    (p) => getEstadoInfo(p).enVivo
  ).length;

  return (
    <div className="calendario-container">
      <div className="calendario-background">
        <div className="calendario-wrapper">
          <TopBar user={user} onLogout={handleLogout} showBackButton={true} />

          <div className="calendario-header">
            <h1 className="calendario-title">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              Calendario de Partidos
            </h1>
            {refreshing && (
              <span className="refresh-indicator">
                <svg className="spinner" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"></path>
                </svg>
                Actualizando...
              </span>
            )}
          </div>

          <div className="calendario-nav">
            <button
              className="nav-btn"
              onClick={() => navigateFecha('prev')}
              disabled={fechasDisponibles.indexOf(fechaKeyActual) <= 0 && fechasDisponibles.length > 0}
              title="Día anterior"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="15 18 9 12 15 6"></polyline>
              </svg>
            </button>

            <div className="fecha-display">
              <span className="fecha-larga">{formatearFechaLarga(fechaSeleccionada)}</span>
              <input
                type="date"
                className="fecha-picker"
                value={fechaPickerValue}
                onChange={handleDateChange}
              />
            </div>

            <button
              className="nav-btn"
              onClick={() => navigateFecha('next')}
              disabled={
                fechasDisponibles.indexOf(fechaKeyActual) >= fechasDisponibles.length - 1 &&
                fechasDisponibles.length > 0
              }
              title="Día siguiente"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </button>
          </div>

          {enVivoCount > 0 && (
            <div className="en-vivo-banner">
              <span className="live-dot"></span>
              <span>{enVivoCount} partido{enVivoCount > 1 ? 's' : ''} en vivo en esta fecha</span>
            </div>
          )}

          <div className="calendario-content">
            {loading ? (
              <div className="loading-container">
                <div className="loading-spinner"></div>
                <p>Cargando calendario...</p>
              </div>
            ) : error ? (
              <div className="error-message">{error}</div>
            ) : partidosDelDia.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">
                  <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="2" y1="12" x2="22" y2="12"></line>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                  </svg>
                </div>
                <h3>No hay partidos para esta fecha</h3>
                <p>Usa las flechas para navegar entre fechas con partidos disponibles.</p>
              </div>
            ) : (
              <div className="partidos-lista">
                {partidosDelDia.map((partido) => {
                  const estado = getEstadoInfo(partido);
                  return (
                    <div
                      key={partido.id_partido}
                      className={`partido-row ${estado.clase}`}
                      onClick={() =>
                        estado.enVivo && handleIrMarcador(partido.id_partido)
                      }
                      style={{ cursor: estado.enVivo ? 'pointer' : 'default' }}
                    >
                      <div className="partido-hora">{formatearHora(partido.horario)}</div>

                      <div className="partido-equipos-row">
                        <div className="equipo-row">
                          {getSeleccionBandera(partido.equipo_local) && (
                            <img
                              src={getSeleccionBandera(partido.equipo_local)}
                              alt=""
                              className="equipo-bandera-row"
                            />
                          )}
                          <span className="equipo-nombre-row">
                            {getSeleccionNombre(partido.equipo_local)}
                          </span>
                        </div>

                        <div className="partido-marcador-row">
                          {partido.gol_local !== undefined && partido.gol_local !== null ? (
                            <>
                              <span className="marcador-goles">{partido.gol_local}</span>
                              <span className="marcador-sep">-</span>
                              <span className="marcador-goles">{partido.gol_visitante}</span>
                            </>
                          ) : (
                            <span className="marcador-vs">VS</span>
                          )}
                        </div>

                        <div className="equipo-row">
                          <span className="equipo-nombre-row">
                            {getSeleccionNombre(partido.equipo_visitante)}
                          </span>
                          {getSeleccionBandera(partido.equipo_visitante) && (
                            <img
                              src={getSeleccionBandera(partido.equipo_visitante)}
                              alt=""
                              className="equipo-bandera-row"
                            />
                          )}
                        </div>
                      </div>

                      <div className={`estado-tag ${estado.clase}`}>
                        {estado.enVivo && <span className="live-pulse"></span>}
                        {estado.texto}
                      </div>

                      <div className="partido-tipo-row">{partido.tipo_partido}</div>

                      {estado.enVivo && (
                        <div className="ir-marcador-hint">
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                            <line x1="8" y1="21" x2="16" y2="21"></line>
                            <line x1="12" y1="17" x2="12" y2="21"></line>
                          </svg>
                          Ver marcador
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {fechasDisponibles.length > 0 && (
            <div className="fechas-quick-bar">
              {fechasDisponibles.slice(0, 14).map((fechaKey) => {
                const fecha = new Date(fechaKey + 'T00:00:00');
                const isActive = fechaKey === fechaKeyActual;
                const tieneEnVivo = (partidosPorFecha[fechaKey] || []).some(
                  (p) => getEstadoInfo(p).enVivo
                );
                return (
                  <button
                    key={fechaKey}
                    className={`fecha-chip ${isActive ? 'active' : ''} ${tieneEnVivo ? 'con-vivo' : ''}`}
                    onClick={() => setFechaSeleccionada(new Date(fechaKey + 'T00:00:00'))}
                  >
                    {formatearFechaCorta(fecha)}
                    {tieneEnVivo && <span className="chip-live-dot"></span>}
                  </button>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CalendarioPage;
