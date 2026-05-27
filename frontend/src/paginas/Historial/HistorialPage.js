import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import { servicioHistorial } from '../../servicios/servicioHistorial';
import TopBar from '../Partidos/componentes/TopBar';
import './estilos/HistorialPage.css';

const HistorialPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [historial, setHistorial] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('pronosticos');
  const [filtroAcierto, setFiltroAcierto] = useState('todos');

  useEffect(() => {
    cargarHistorial();
  }, []);

  const cargarHistorial = async () => {
    setLoading(true);
    setError(null);
    const result = await servicioHistorial.getHistorialUsuario();
    if (result.success) {
      setHistorial(result.data);
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  const handleLogout = async () => {
    await logout();
    navigate('/home');
  };

  const pronosticosFiltrados = historial?.pronosticos?.filter(p => {
    if (filtroAcierto === 'todos') return true;
    if (filtroAcierto === 'aciertos') return p.puntos_obtenidos > 0;
    if (filtroAcierto === 'fallidos') return p.puntos_obtenidos === 0 && p.estado_partido === 'finalizado';
    if (filtroAcierto === 'pendientes') return p.estado_partido !== 'finalizado';
    return true;
  }) || [];

  const getBadgeClass = (tipo) => {
    switch (tipo) {
      case 'Marcador exacto': return 'badge-exacto';
      case 'Resultado correcto': return 'badge-correcto';
      case 'Fallido': return 'badge-fallido';
      default: return 'badge-pendiente';
    }
  };

  const getEstadoLigaClass = (estado) => {
    if (estado === 'Ganada') return 'estado-ganada';
    if (estado.startsWith('Posición')) return 'estado-posicion';
    return 'estado-sin-posicion';
  };

  if (loading) {
    return (
      <div className="historial-container">
        <div className="historial-background">
          <div className="historial-wrapper">
            <TopBar user={user} onLogout={handleLogout} />
            <div className="loading-container">
              <div className="loading-spinner"></div>
              <p>Cargando historial...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error && !historial) {
    return (
      <div className="historial-container">
        <div className="historial-background">
          <div className="historial-wrapper">
            <TopBar user={user} onLogout={handleLogout} />
            <div className="historial-content">
              <div className="error-message" style={{ marginTop: '40px', justifyContent: 'center' }}>
                <p>{error}</p>
                <button onClick={cargarHistorial} className="retry-button">Reintentar</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="historial-container">
      <div className="historial-background">
        <div className="historial-wrapper">
          <TopBar user={user} onLogout={handleLogout} />

          <div className="historial-content">
            <div className="historial-header">
              <h1>Mi Historial</h1>
              <div className="historial-resumen">
                <div className="resumen-card">
                  <span className="resumen-valor">{historial?.total_pronosticos || 0}</span>
                  <span className="resumen-label">Pronósticos</span>
                </div>
                <div className="resumen-card">
                  <span className="resumen-valor">{historial?.puntos_totales || 0}</span>
                  <span className="resumen-label">Puntos totales</span>
                </div>
                <div className="resumen-card">
                  <span className="resumen-valor">{historial?.resumen_ligas?.length || 0}</span>
                  <span className="resumen-label">Ligas</span>
                </div>
              </div>
            </div>

            {error && (
              <div className="error-message">
                <p>{error}</p>
                <button onClick={cargarHistorial} className="retry-button">Reintentar</button>
              </div>
            )}

            {/* Tabs */}
            <div className="tabs-container">
              <button
                className={`tab-button ${activeTab === 'pronosticos' ? 'active' : ''}`}
                onClick={() => setActiveTab('pronosticos')}
              >
                Pronósticos por Partido
              </button>
              <button
                className={`tab-button ${activeTab === 'ligas' ? 'active' : ''}`}
                onClick={() => setActiveTab('ligas')}
              >
                Mis Ligas
              </button>
            </div>

            {/* Tab Pronósticos */}
            {activeTab === 'pronosticos' && (
              <div className="tab-content">
                <div className="filtros-row">
                  <label>Filtrar:</label>
                  <select value={filtroAcierto} onChange={(e) => setFiltroAcierto(e.target.value)}>
                    <option value="todos">Todos</option>
                    <option value="aciertos">Aciertos</option>
                    <option value="fallidos">Fallidos</option>
                    <option value="pendientes">Pendientes</option>
                  </select>
                </div>

                {pronosticosFiltrados.length === 0 ? (
                  <div className="empty-state">
                    <h3>No hay pronósticos</h3>
                    <p>Aún no tienes pronósticos registrados o no coinciden con el filtro seleccionado.</p>
                  </div>
                ) : (
                  <div className="pronosticos-lista">
                    {pronosticosFiltrados.map((p) => (
                      <div key={p.id_pronostico} className="pronostico-card">
                        <div className="pronostico-header">
                          <div className="equipos">
                            <span className="equipo">{p.equipo_local}</span>
                            <span className="vs">vs</span>
                            <span className="equipo">{p.equipo_visitante}</span>
                          </div>
                          <span className={`badge ${getBadgeClass(p.tipo_acierto)}`}>
                            {p.tipo_acierto}
                          </span>
                        </div>

                        <div className="pronostico-marcadores">
                          <div className="marcador-row">
                            <span className="label">Tu pronóstico:</span>
                            <span className="valor">{p.resultado_pronosticado}</span>
                          </div>
                          <div className="marcador-row">
                            <span className="label">Resultado real:</span>
                            <span className="valor real">{p.resultado_real}</span>
                          </div>
                        </div>

                        <div className="pronostico-footer">
                          <span className="puntos">+{p.puntos_obtenidos} pts</span>
                          <span className="estado">{p.estado_partido}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Tab Ligas */}
            {activeTab === 'ligas' && (
              <div className="tab-content">
                {historial?.resumen_ligas?.length === 0 ? (
                  <div className="empty-state">
                    <h3>No hay ligas</h3>
                    <p>Aún no participas en ninguna liga.</p>
                  </div>
                ) : (
                  <div className="ligas-lista">
                    {historial.resumen_ligas.map((liga) => (
                      <div key={liga.liga_id} className="liga-card">
                        <div className="liga-header">
                          <h3>{liga.liga_nombre}</h3>
                          <span className={`estado-liga ${getEstadoLigaClass(liga.estado_liga)}`}>
                            {liga.estado_liga}
                          </span>
                        </div>

                        <div className="liga-stats">
                          <div className="stat">
                            <span className="stat-valor">{liga.puntos_totales}</span>
                            <span className="stat-label">Puntos</span>
                          </div>
                          <div className="stat">
                            <span className="stat-valor">{liga.partidos_jugados}</span>
                            <span className="stat-label">Partidos</span>
                          </div>
                          <div className="stat">
                            <span className="stat-valor">{liga.marcadores_exactos}</span>
                            <span className="stat-label">Exactos</span>
                          </div>
                          <div className="stat">
                            <span className="stat-valor">{liga.resultados_correctos}</span>
                            <span className="stat-label">Resultados</span>
                          </div>
                          <div className="stat">
                            <span className="stat-valor">{liga.fallidos}</span>
                            <span className="stat-label">Fallidos</span>
                          </div>
                        </div>

                        <div className="liga-barra">
                          {liga.partidos_jugados > 0 && (
                            <>
                              <div
                                className="barra-exacto"
                                style={{ width: `${(liga.marcadores_exactos / liga.partidos_jugados) * 100}%` }}
                              />
                              <div
                                className="barra-correcto"
                                style={{ width: `${(liga.resultados_correctos / liga.partidos_jugados) * 100}%` }}
                              />
                              <div
                                className="barra-fallido"
                                style={{ width: `${(liga.fallidos / liga.partidos_jugados) * 100}%` }}
                              />
                            </>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HistorialPage;
