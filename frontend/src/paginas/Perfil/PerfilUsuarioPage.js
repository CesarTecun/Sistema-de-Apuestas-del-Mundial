import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import { servicioHistorial } from '../../servicios/servicioHistorial';
import servicioLigas from '../../servicios/servicioLigas';
import TopBar from '../../componentes/TopBar';
import PerfilHeader from './componentes/PerfilHeader';
import BuzonInvitaciones from './componentes/BuzonInvitaciones';
import useNotificaciones from '../../hooks/useNotificaciones';
import NotificacionesContainer from '../../componentes/NotificacionesContainer';
import './estilos/PerfilUsuarioPage.css';

const PerfilUsuarioPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const {
    notificaciones,
    cerrarNotificacion,
    success,
    error: mostrarError
  } = useNotificaciones();
  
  const [historial, setHistorial] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('pronosticos');
  const [filtroAcierto, setFiltroAcierto] = useState('todos');
  const [hasVisited, setHasVisited] = useState(false);
  const [ligasUsuario, setLigasUsuario] = useState([]);
  const [ligasLoading, setLigasLoading] = useState(false);
  const [invitaciones, setInvitaciones] = useState([]);
  const [invitacionesLoading, setInvitacionesLoading] = useState(false);
  const [misLigasExpanded, setMisLigasExpanded] = useState(false);

  useEffect(() => {
    const visited = sessionStorage.getItem('perfil_visited');
    if (visited) {
      setHasVisited(true);
    } else {
      sessionStorage.setItem('perfil_visited', 'true');
    }
  }, []);

  useEffect(() => {
    cargarHistorial();
    cargarInvitaciones();
    cargarLigasUsuario();
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

  const cargarLigasUsuario = async () => {
    setLigasLoading(true);
    try {
      const result = await servicioLigas.getLigas();
      if (result.success) {
        setLigasUsuario(result.data);
      }
    } catch (error) {
      console.error('Error al cargar ligas:', error);
    } finally {
      setLigasLoading(false);
    }
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

  const cargarInvitaciones = async () => {
    setInvitacionesLoading(true);
    try {
      const result = await servicioLigas.getInvitaciones();
      if (result.success) {
        setInvitaciones(result.data.results || result.data);
      }
    } catch (error) {
      console.error('Error al cargar invitaciones:', error);
    } finally {
      setInvitacionesLoading(false);
    }
  };

  const handleInvitacionAceptada = () => {
    cargarInvitaciones();
    cargarHistorial();
    // success('Invitación procesada correctamente');
  };

  const handleInvitacionError = (errorMessage) => {
    mostrarError(errorMessage);
  };

  return (
    <div className={`perfil-container ${hasVisited ? 'no-animation' : ''}`}>
      <div className="perfil-background">
        <div className="perfil-wrapper">
          <div className="main-sticky-container">
            <TopBar user={user} onLogout={handleLogout} showBackButton={true} />
            
            <div className="sticky-controls">
              <PerfilHeader user={user} />
            </div>
          </div>

          <div className="perfil-content">
            {loading && (
              <div className="loading-container">
                <div className="loading-spinner"></div>
                <p>Cargando perfil...</p>
              </div>
            )}

            {error && !historial && (
              <div className="error-message">
                <p>{error}</p>
                <button onClick={cargarHistorial} className="retry-button">Reintentar</button>
              </div>
            )}

            {!loading && !error && (
              <>
                {/* Stats Grid */}
                <div className="perfil-stats-grid">
                  <div className="perfil-stat-card">
                    <div className="stat-icon-wrapper" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                        <path d="M12 20h9"></path>
                        <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                      </svg>
                    </div>
                    <div className="stat-content">
                      <span className="stat-value">{historial?.total_pronosticos || 0}</span>
                      <span className="stat-label">Pronósticos</span>
                    </div>
                  </div>
                  
                  <div className="perfil-stat-card">
                    <div className="stat-icon-wrapper" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                      </svg>
                    </div>
                    <div className="stat-content">
                      <span className="stat-value">{historial?.puntos_totales || 0}</span>
                      <span className="stat-label">Puntos totales</span>
                    </div>
                  </div>
                  
                  <div className="perfil-stat-card">
                    <div className="stat-icon-wrapper" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }}>
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                        <circle cx="9" cy="7" r="4"></circle>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                      </svg>
                    </div>
                    <div className="stat-content">
                      <span className="stat-value">{historial?.resumen_ligas?.length || 0}</span>
                      <span className="stat-label">Ligas</span>
                    </div>
                  </div>
                  
                  <div className="perfil-stat-card">
                    <div className="stat-icon-wrapper" style={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' }}>
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                        <polyline points="22 4 12 14.01 9 11.01"></polyline>
                      </svg>
                    </div>
                    <div className="stat-content">
                      <span className="stat-value">
                        {historial?.pronosticos?.filter(p => p.puntos_obtenidos > 0).length || 0}
                      </span>
                      <span className="stat-label">Aciertos</span>
                    </div>
                  </div>
                </div>

                {/* Mis Ligas Section */}
                <div className="mis-ligas-section">
                  <div className="section-header" onClick={() => setMisLigasExpanded(!misLigasExpanded)}>
                    <h2 className="section-title">Mis Ligas</h2>
                    <svg 
                      className={`chevron-icon ${misLigasExpanded ? 'expanded' : ''}`}
                      width="20" 
                      height="20" 
                      viewBox="0 0 24 24" 
                      fill="none" 
                      stroke="currentColor" 
                      strokeWidth="2"
                    >
                      <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                  </div>
                  {misLigasExpanded && (
                    <div className="section-content">
                      {ligasLoading ? (
                        <div className="empty-state-compact">
                          <p>Cargando ligas...</p>
                        </div>
                      ) : !ligasUsuario || ligasUsuario.length === 0 ? (
                        <div className="empty-state-compact">
                          <div className="empty-icon">
                            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                              <circle cx="9" cy="7" r="4"></circle>
                              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                            </svg>
                          </div>
                          <p>Aún no participas en ninguna liga.</p>
                        </div>
                      ) : (
                        <div className="ligas-compact-grid">
                          {ligasUsuario.map((liga) => {
                            const ligaHistorial = historial?.resumen_ligas?.find(h => h.liga_id === liga.id_liga);
                            return (
                              <div key={liga.id_liga} className="liga-compact-card">
                                <div className="liga-compact-header">
                                  <h3>{liga.nombre_liga}</h3>
                                  <span className="liga-compact-status" style={{ background: 'linear-gradient(135deg, #a83279 0%, #6a4c93 100%)' }}>
                                    {liga.tipo_liga}
                                  </span>
                                </div>
                                <div className="liga-compact-stats">
                                  <div className="compact-stat">
                                    <span className="compact-stat-label">Puntos</span>
                                    <span className="compact-stat-value">{ligaHistorial?.puntos_totales || 0}</span>
                                  </div>
                                  <div className="compact-stat">
                                    <span className="compact-stat-label">Partidos</span>
                                    <span className="compact-stat-value">{ligaHistorial?.partidos_jugados || 0}</span>
                                  </div>
                                  <div className="compact-stat">
                                    <span className="compact-stat-label">Exactos</span>
                                    <span className="compact-stat-value">{ligaHistorial?.marcadores_exactos || 0}</span>
                                  </div>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Buzón de Invitaciones */}
                <BuzonInvitaciones 
                  invitaciones={invitaciones}
                  loading={invitacionesLoading}
                  onInvitacionAceptada={handleInvitacionAceptada}
                  onInvitacionError={handleInvitacionError}
                />

                {/* Tabs */}
                <div className="perfil-tabs">
                  <button
                    className={`perfil-tab ${activeTab === 'pronosticos' ? 'active' : ''}`}
                    onClick={() => setActiveTab('pronosticos')}
                  >
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                      <polyline points="14 2 14 8 20 8"></polyline>
                      <line x1="16" y1="13" x2="8" y2="13"></line>
                      <line x1="16" y1="17" x2="8" y2="17"></line>
                      <polyline points="10 9 9 9 8 9"></polyline>
                    </svg>
                    Pronósticos
                  </button>
                  <button
                    className={`perfil-tab ${activeTab === 'ligas' ? 'active' : ''}`}
                    onClick={() => setActiveTab('ligas')}
                  >
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                      <circle cx="9" cy="7" r="4"></circle>
                      <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                      <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                    </svg>
                    Mis Ligas
                  </button>
                </div>

                {/* Tab Content */}
                {activeTab === 'pronosticos' && (
                  <div className="perfil-tab-content">
                    <div className="perfil-filters">
                      <label>Filtrar por:</label>
                      <div className="filter-buttons">
                        <button 
                          className={`filter-btn ${filtroAcierto === 'todos' ? 'active' : ''}`}
                          onClick={() => setFiltroAcierto('todos')}
                        >
                          Todos
                        </button>
                        <button 
                          className={`filter-btn ${filtroAcierto === 'aciertos' ? 'active' : ''}`}
                          onClick={() => setFiltroAcierto('aciertos')}
                        >
                          Aciertos
                        </button>
                        <button 
                          className={`filter-btn ${filtroAcierto === 'fallidos' ? 'active' : ''}`}
                          onClick={() => setFiltroAcierto('fallidos')}
                        >
                          Fallidos
                        </button>
                        <button 
                          className={`filter-btn ${filtroAcierto === 'pendientes' ? 'active' : ''}`}
                          onClick={() => setFiltroAcierto('pendientes')}
                        >
                          Pendientes
                        </button>
                      </div>
                    </div>

                    {pronosticosFiltrados.length === 0 ? (
                      <div className="empty-state">
                        <div className="empty-icon">
                          <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                            <path d="M9 11l3 3L22 4"></path>
                            <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
                          </svg>
                        </div>
                        <h3>No hay pronósticos</h3>
                        <p>Aún no tienes pronósticos registrados o no coinciden con el filtro seleccionado.</p>
                      </div>
                    ) : (
                      <div className="pronosticos-grid">
                        {pronosticosFiltrados.map((p) => (
                          <div key={p.id_pronostico} className="pronostico-card-new">
                            <div className="pronostico-match">
                              <span className="team-name">{p.equipo_local}</span>
                              <span className="match-vs">VS</span>
                              <span className="team-name">{p.equipo_visitante}</span>
                            </div>
                            <div className="pronostico-details">
                              <div className="detail-row">
                                <span className="detail-label">Tu pronóstico:</span>
                                <span className="detail-value">{p.resultado_pronosticado}</span>
                              </div>
                              <div className="detail-row">
                                <span className="detail-label">Resultado real:</span>
                                <span className="detail-value actual">{p.resultado_real}</span>
                              </div>
                            </div>
                            <div className="pronostico-footer-new">
                              <span className={`badge-new ${getBadgeClass(p.tipo_acierto)}`}>
                                {p.tipo_acierto}
                              </span>
                              <div className="points-status">
                                <span className="points">+{p.puntos_obtenidos} pts</span>
                                <span className="status">{p.estado_partido}</span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {activeTab === 'ligas' && (
                  <div className="perfil-tab-content">
                    {historial?.resumen_ligas?.length === 0 ? (
                      <div className="empty-state">
                        <div className="empty-icon">
                          <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                            <circle cx="9" cy="7" r="4"></circle>
                            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                          </svg>
                        </div>
                        <h3>No hay ligas</h3>
                        <p>Aún no participas en ninguna liga.</p>
                      </div>
                    ) : (
                      <div className="ligas-grid-new">
                        {historial.resumen_ligas.map((liga) => (
                          <div key={liga.liga_id} className="liga-card-new">
                            <div className="liga-card-header">
                              <h3>{liga.liga_nombre}</h3>
                              <span className={`liga-status ${getEstadoLigaClass(liga.estado_liga)}`}>
                                {liga.estado_liga}
                              </span>
                            </div>
                            <div className="liga-stats-grid">
                              <div className="mini-stat">
                                <span className="mini-stat-value">{liga.puntos_totales}</span>
                                <span className="mini-stat-label">Puntos</span>
                              </div>
                              <div className="mini-stat">
                                <span className="mini-stat-value">{liga.partidos_jugados}</span>
                                <span className="mini-stat-label">Partidos</span>
                              </div>
                              <div className="mini-stat">
                                <span className="mini-stat-value">{liga.marcadores_exactos}</span>
                                <span className="mini-stat-label">Exactos</span>
                              </div>
                              <div className="mini-stat">
                                <span className="mini-stat-value">{liga.resultados_correctos}</span>
                                <span className="mini-stat-label">Resultados</span>
                              </div>
                              <div className="mini-stat">
                                <span className="mini-stat-value">{liga.fallidos}</span>
                                <span className="mini-stat-label">Fallidos</span>
                              </div>
                            </div>
                            {liga.partidos_jugados > 0 && (
                              <div className="liga-progress-bar">
                                <div className="progress-segment exacto" style={{ width: `${(liga.marcadores_exactos / liga.partidos_jugados) * 100}%` }} />
                                <div className="progress-segment correcto" style={{ width: `${(liga.resultados_correctos / liga.partidos_jugados) * 100}%` }} />
                                <div className="progress-segment fallido" style={{ width: `${(liga.fallidos / liga.partidos_jugados) * 100}%` }} />
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </>
            )}
          </div>
        </div>

        <NotificacionesContainer 
          notificaciones={notificaciones}
          onClose={cerrarNotificacion}
        />
      </div>
    </div>
  );
};

export default PerfilUsuarioPage;
