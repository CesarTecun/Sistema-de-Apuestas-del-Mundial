import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import servicioMarcador from '../../servicios/servicioMarcador';
import servicioLigas from '../../servicios/servicioLigas';
import servicioSelecciones from '../../servicios/servicioSelecciones';
import TopBar from '../Ligas/componentes/TopBar';
import useNotificaciones from '../../hooks/useNotificaciones';
import NotificacionesContainer from '../../componentes/NotificacionesContainer';
import './estilos/MarcadorPage.css';

const MarcadorPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { notificaciones, cerrarNotificacion, success, error: mostrarError } = useNotificaciones();

  // Estados de carga y datos
  const [loading, setLoading] = useState(true);
  const [partidos, setPartidos] = useState([]);
  const [selecciones, setSelecciones] = useState([]);
  const [ligas, setLigas] = useState([]);
  const [activeTab, setActiveTab] = useState('programado'); // 'programado', 'en_juego', 'finalizado'

  // Modales
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showScoreModal, setShowScoreModal] = useState(false);
  const [selectedPartido, setSelectedPartido] = useState(null);

  // Formulario de creación
  const [createForm, setCreateForm] = useState({
    horario: '',
    equipo_local: '',
    equipo_visitante: '',
    fk_id_liga: '',
    tipo_partido: 'Regular',
    fk_sede: '',
    fk_id_fase: ''
  });

  // Formulario de actualización de marcador
  const [scoreForm, setScoreForm] = useState({
    gol_local: 0,
    gol_visitante: 0,
    estado: 'en_juego',
    ganador_penales: ''
  });

  const isAdmin = user?.fk_rol === 1;

  const cargarDatos = useCallback(async () => {
    setLoading(true);
    try {
      const [resPartidos, resSelecciones, resLigas] = await Promise.all([
        servicioMarcador.getPartidos(),
        servicioSelecciones.getSelecciones(),
        servicioLigas.getLigas()
      ]);

      if (resPartidos.success) setPartidos(resPartidos.data);
      if (resSelecciones.success) setSelecciones(resSelecciones.data);
      if (resLigas.success) setLigas(resLigas.data);
    } catch (err) {
      console.error(err);
      mostrarError('Error de red al sincronizar con los servicios del marcador.');
    } finally {
      setLoading(false);
    }
  }, [mostrarError]);

  const refrescarPartidos = useCallback(async () => {
    const res = await servicioMarcador.getPartidos();
    if (res.success) {
      setPartidos(res.data);
    }
  }, []);

  // Cargar datos al montar
  useEffect(() => {
    cargarDatos();
    
    // Intervalo para actualizar marcadores en vivo cada 10 segundos de forma pasiva
    const timer = setInterval(() => {
      refrescarPartidos();
    }, 10000);

    return () => clearInterval(timer);
  }, [cargarDatos, refrescarPartidos]);

  const handleLogout = async () => {
    await logout();
    navigate('/home');
  };

  // Filtrar partidos según la pestaña activa
  const partidosFiltrados = partidos.filter(p => p.estado === activeTab);

  // Helper para buscar los detalles de la selección (bandera, país) por id
  const getDetallesSeleccion = (idSeleccion) => {
    return selecciones.find(s => s.id_seleccion === idSeleccion) || { pais: `Equipo ${idSeleccion}`, bandera: '🏳️' };
  };

  // Formatear horario de manera elegante
  const formatearFecha = (isoString) => {
    if (!isoString) return '';
    try {
      const fecha = new Date(isoString);
      return fecha.toLocaleDateString('es-ES', {
        weekday: 'short',
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (e) {
      return isoString;
    }
  };

  // --- Operaciones de Administrador ---

  const handleCreatePartido = async (e) => {
    e.preventDefault();
    if (!createForm.equipo_local || !createForm.equipo_visitante || !createForm.horario) {
      mostrarError('Por favor completa los campos obligatorios.');
      return;
    }

    if (createForm.equipo_local === createForm.equipo_visitante) {
      mostrarError('El equipo local y visitante no pueden ser el mismo.');
      return;
    }

    const payload = {
      horario: new Date(createForm.horario).toISOString(),
      equipo_local: parseInt(createForm.equipo_local),
      equipo_visitante: parseInt(createForm.equipo_visitante),
      fk_id_liga: createForm.fk_id_liga ? parseInt(createForm.fk_id_liga) : null,
      tipo_partido: createForm.tipo_partido,
      fk_sede: createForm.fk_sede ? parseInt(createForm.fk_sede) : null,
      fk_id_fase: createForm.fk_id_fase ? parseInt(createForm.fk_id_fase) : null,
      estado: 'programado',
      gol_local: 0,
      gol_visitante: 0
    };

    const res = await servicioMarcador.createPartido(payload);
    if (res.success) {
      success('Partido creado y sincronizado en el microservicio.');
      setShowCreateModal(false);
      // Limpiar formulario
      setCreateForm({
        horario: '',
        equipo_local: '',
        equipo_visitante: '',
        fk_id_liga: '',
        tipo_partido: 'Regular',
        fk_sede: '',
        fk_id_fase: ''
      });
      refrescarPartidos();
    } else {
      mostrarError(res.error || 'Error al crear partido.');
    }
  };

  const handleIniciarPartido = async (idPartido) => {
    // Iniciar partido: estado "en_juego", goles en 0
    const res = await servicioMarcador.actualizarMarcador(idPartido, 0, 0, 'en_juego', '0 - 0', null);
    if (res.success) {
      success('¡Partido iniciado en tiempo real!');
      refrescarPartidos();
      setActiveTab('en_juego');
    } else {
      mostrarError(res.error || 'No se pudo iniciar el partido.');
    }
  };

  const openScoreModal = (partido) => {
    setSelectedPartido(partido);
    setScoreForm({
      gol_local: partido.gol_local,
      gol_visitante: partido.gol_visitante,
      estado: partido.estado,
      ganador_penales: partido.ganador_penales || ''
    });
    setShowScoreModal(true);
  };

  const handleUpdateScore = async (e) => {
    e.preventDefault();
    if (!selectedPartido) return;

    const res = await servicioMarcador.actualizarMarcador(
      selectedPartido.id_partido,
      parseInt(scoreForm.gol_local),
      parseInt(scoreForm.gol_visitante),
      scoreForm.estado,
      `${scoreForm.gol_local} - ${scoreForm.gol_visitante}`,
      scoreForm.ganador_penales ? parseInt(scoreForm.ganador_penales) : null
    );

    if (res.success) {
      success('Marcador actualizado exitosamente.');
      setShowScoreModal(false);
      refrescarPartidos();
      if (scoreForm.estado !== selectedPartido.estado) {
        setActiveTab(scoreForm.estado);
      }
    } else {
      mostrarError(res.error || 'Error al actualizar marcador.');
    }
  };

  const handleDeletePartido = async (idPartido) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este partido del microservicio?')) {
      const res = await servicioMarcador.deletePartido(idPartido);
      if (res.success) {
        success('Partido eliminado.');
        refrescarPartidos();
      } else {
        mostrarError(res.error || 'Error al eliminar partido.');
      }
    }
  };

  return (
    <div className="marcador-container">
      <div className="marcador-background">
        <div className="marcador-wrapper">
          <TopBar user={user} onLogout={handleLogout} />

          <div className="marcador-header">
            <h1 className="marcador-title">
              Marcadores en Vivo
            </h1>
            {isAdmin && (
              <button className="marcador-btn-nuevo" onClick={() => setShowCreateModal(true)}>
                Nuevo Partido
              </button>
            )}
          </div>

          <div className="marcador-content">
            {/* Selector de pestañas */}
            <div className="marcador-tabs">
              <button 
                className={`marcador-tab ${activeTab === 'programado' ? 'active' : ''}`}
                onClick={() => setActiveTab('programado')}
              >
                Programados
              </button>
              <button 
                className={`marcador-tab ${activeTab === 'en_juego' ? 'active' : ''}`}
                onClick={() => setActiveTab('en_juego')}
              >
                En Vivo
              </button>
              <button 
                className={`marcador-tab ${activeTab === 'finalizado' ? 'active' : ''}`}
                onClick={() => setActiveTab('finalizado')}
              >
                Finalizados
              </button>
            </div>

            {loading ? (
              <div className="loading-container">
                <div className="loading-spinner"></div>
                <p>Cargando marcadores en vivo...</p>
              </div>
            ) : (
              <>
                {partidosFiltrados.length === 0 ? (
                  <div className="empty-state">
                    <h3>No hay partidos en esta categoría</h3>
                    <p>Las actualizaciones en tiempo real aparecerán aquí automáticamente.</p>
                  </div>
                ) : (
                  <div className="marcador-grid">
                    {partidosFiltrados.map((partido) => {
                      const local = partido.equipo_local_detalle || getDetallesSeleccion(partido.equipo_local);
                      const visitante = partido.equipo_visitante_detalle || getDetallesSeleccion(partido.equipo_visitante);

                      return (
                        <div 
                          key={partido.id_partido} 
                          className={`tarjeta-marcador ${partido.estado === 'en_juego' ? 'live' : partido.estado === 'finalizado' ? 'finished' : 'scheduled'}`}
                        >
                          <div className="partido-marcador-header">
                            <span className={`partido-marcador-estado ${partido.estado === 'en_juego' ? 'live' : partido.estado === 'finalizado' ? 'finished' : 'scheduled'}`}>
                              {partido.estado === 'en_juego' && <span className="pulse-dot"></span>}
                              {partido.estado === 'en_juego' ? 'En Vivo' : partido.estado === 'finalizado' ? 'Finalizado' : 'Programado'}
                            </span>
                            <span className="partido-marcador-tipo">
                              {partido.tipo_partido}
                            </span>
                          </div>

                          <div className="partido-marcador-equipos">
                            <div className="equipo-marcador">
                              {local.bandera && local.bandera.startsWith('http') ? (
                                <img src={local.bandera} alt={local.pais} className="equipo-marcador-bandera-img" />
                              ) : (
                                <span className="equipo-marcador-bandera">{local.bandera || '🏳️'}</span>
                              )}
                              <span className="equipo-marcador-nombre">{local.pais}</span>
                            </div>

                            <div className="goles-visualizador">
                              {partido.estado === 'programado' ? (
                                <span className="vs-texto">VS</span>
                              ) : (
                                <div className="goles-numeros">
                                  <span className="goles-local">{partido.gol_local}</span>
                                  <span className="goles-separador">-</span>
                                  <span className="goles-visitante">{partido.gol_visitante}</span>
                                </div>
                              )}
                              <span style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '8px' }}>
                                {formatearFecha(partido.horario)}
                              </span>
                            </div>

                            <div className="equipo-marcador">
                              {visitante.bandera && visitante.bandera.startsWith('http') ? (
                                <img src={visitante.bandera} alt={visitante.pais} className="equipo-marcador-bandera-img" />
                              ) : (
                                <span className="equipo-marcador-bandera">{visitante.bandera || '🏳️'}</span>
                              )}
                              <span className="equipo-marcador-nombre">{visitante.pais}</span>
                            </div>
                          </div>

                          {/* Acciones del Administrador */}
                          {isAdmin && (
                            <div className="partido-marcador-acciones">
                              {partido.estado === 'programado' && (
                                <button 
                                  className="btn-marcador btn-marcador-iniciar"
                                  onClick={() => handleIniciarPartido(partido.id_partido)}
                                >
                                  Iniciar
                                </button>
                              )}
                              {partido.estado === 'en_juego' && (
                                <button 
                                  className="btn-marcador btn-marcador-actualizar"
                                  onClick={() => openScoreModal(partido)}
                                >
                                  Marcador
                                </button>
                              )}
                              {partido.estado === 'en_juego' && (
                                <button 
                                  className="btn-marcador btn-marcador-finalizar"
                                  onClick={() => {
                                    setSelectedPartido(partido);
                                    setScoreForm({
                                      gol_local: partido.gol_local,
                                      gol_visitante: partido.gol_visitante,
                                      estado: 'finalizado',
                                      ganador_penales: partido.ganador_penales || ''
                                    });
                                    setShowScoreModal(true);
                                  }}
                                >
                                  Finalizar
                                </button>
                              )}
                              {partido.estado === 'finalizado' && (
                                <button 
                                  className="btn-marcador btn-marcador-actualizar"
                                  onClick={() => openScoreModal(partido)}
                                >
                                  Corregir
                                </button>
                              )}
                              <button 
                                className="btn-marcador btn-marcador-eliminar"
                                onClick={() => handleDeletePartido(partido.id_partido)}
                              >
                                Eliminar
                              </button>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>

      {/* MODAL: Crear Partido */}
      {showCreateModal && (
        <div className="marcador-modal-overlay">
          <div className="marcador-modal">
            <button className="marcador-modal-close" onClick={() => setShowCreateModal(false)}>×</button>
            <h2>Crear Partido (Marcador)</h2>
            <form onSubmit={handleCreatePartido}>
              <label style={{ display: 'block', marginBottom: '6px', fontWeight: 'bold' }}>Equipo Local *</label>
              <select 
                className="marcador-select"
                value={createForm.equipo_local}
                onChange={(e) => setCreateForm({ ...createForm, equipo_local: e.target.value })}
                required
              >
                <option value="">Seleccione equipo local...</option>
                {selecciones.map(s => (
                  <option key={s.id_seleccion} value={s.id_seleccion}>
                    {s.bandera} {s.pais}
                  </option>
                ))}
              </select>

              <label style={{ display: 'block', marginBottom: '6px', fontWeight: 'bold' }}>Equipo Visitante *</label>
              <select 
                className="marcador-select"
                value={createForm.equipo_visitante}
                onChange={(e) => setCreateForm({ ...createForm, equipo_visitante: e.target.value })}
                required
              >
                <option value="">Seleccione equipo visitante...</option>
                {selecciones.map(s => (
                  <option key={s.id_seleccion} value={s.id_seleccion}>
                    {s.bandera} {s.pais}
                  </option>
                ))}
              </select>

              <label style={{ display: 'block', marginBottom: '6px', fontWeight: 'bold' }}>Liga (Opcional)</label>
              <select 
                className="marcador-select"
                value={createForm.fk_id_liga}
                onChange={(e) => setCreateForm({ ...createForm, fk_id_liga: e.target.value })}
              >
                <option value="">Seleccione liga...</option>
                {ligas.map(l => (
                  <option key={l.id_liga} value={l.id_liga}>
                    {l.nombre}
                  </option>
                ))}
              </select>

              <label style={{ display: 'block', marginBottom: '6px', fontWeight: 'bold' }}>Horario *</label>
              <input 
                type="datetime-local" 
                className="marcador-input-fecha"
                value={createForm.horario}
                onChange={(e) => setCreateForm({ ...createForm, horario: e.target.value })}
                required
              />

              <div style={{ display: 'flex', gap: '12px' }}>
                <div style={{ flex: 1 }}>
                  <label style={{ display: 'block', marginBottom: '6px', fontWeight: 'bold' }}>Tipo Partido</label>
                  <select 
                    className="marcador-select"
                    value={createForm.tipo_partido}
                    onChange={(e) => setCreateForm({ ...createForm, tipo_partido: e.target.value })}
                  >
                    <option value="Regular">Regular</option>
                    <option value="Octavos">Octavos de Final</option>
                    <option value="Cuartos">Cuartos de Final</option>
                    <option value="Semifinal">Semifinal</option>
                    <option value="Final">Final</option>
                  </select>
                </div>
              </div>

              <div className="marcador-form-acciones">
                <button type="button" className="marcador-btn-cancelar" onClick={() => setShowCreateModal(false)}>
                  Cancelar
                </button>
                <button type="submit" className="marcador-btn-guardar">
                  Crear
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL: Actualizar Marcador / Finalizar */}
      {showScoreModal && selectedPartido && (
        <div className="marcador-modal-overlay">
          <div className="marcador-modal">
            <button className="marcador-modal-close" onClick={() => setShowScoreModal(false)}>×</button>
            <h2>Actualizar Partido</h2>
            
            <div style={{ textAlign: 'center', marginBottom: '20px' }}>
              <span style={{ fontSize: '24px' }}>
                {getDetallesSeleccion(selectedPartido.equipo_local).bandera} vs {getDetallesSeleccion(selectedPartido.equipo_visitante).bandera}
              </span>
              <p style={{ margin: '5px 0', fontWeight: 'bold' }}>
                {getDetallesSeleccion(selectedPartido.equipo_local).pais} vs {getDetallesSeleccion(selectedPartido.equipo_visitante).pais}
              </p>
            </div>

            <form onSubmit={handleUpdateScore}>
              <div className="control-goles-form">
                <div className="control-goles-selector">
                  <span style={{ fontSize: '12px', opacity: 0.8 }}>Goles Local</span>
                  <button 
                    type="button" 
                    className="btn-goles-cambiar"
                    onClick={() => setScoreForm({ ...scoreForm, gol_local: Math.max(0, scoreForm.gol_local - 1) })}
                  >
                    -
                  </button>
                  <input 
                    type="number" 
                    className="goles-input-numero"
                    value={scoreForm.gol_local}
                    onChange={(e) => setScoreForm({ ...scoreForm, gol_local: Math.max(0, parseInt(e.target.value) || 0) })}
                  />
                  <button 
                    type="button" 
                    className="btn-goles-cambiar"
                    onClick={() => setScoreForm({ ...scoreForm, gol_local: scoreForm.gol_local + 1 })}
                  >
                    +
                  </button>
                </div>

                <span style={{ fontSize: '24px', opacity: 0.5 }}>-</span>

                <div className="control-goles-selector">
                  <span style={{ fontSize: '12px', opacity: 0.8 }}>Goles Visitante</span>
                  <button 
                    type="button" 
                    className="btn-goles-cambiar"
                    onClick={() => setScoreForm({ ...scoreForm, gol_visitante: Math.max(0, scoreForm.gol_visitante - 1) })}
                  >
                    -
                  </button>
                  <input 
                    type="number" 
                    className="goles-input-numero"
                    value={scoreForm.gol_visitante}
                    onChange={(e) => setScoreForm({ ...scoreForm, gol_visitante: Math.max(0, parseInt(e.target.value) || 0) })}
                  />
                  <button 
                    type="button" 
                    className="btn-goles-cambiar"
                    onClick={() => setScoreForm({ ...scoreForm, gol_visitante: scoreForm.gol_visitante + 1 })}
                  >
                    +
                  </button>
                </div>
              </div>

              <label style={{ display: 'block', marginBottom: '6px', fontWeight: 'bold' }}>Estado del Partido</label>
              <select 
                className="marcador-select"
                value={scoreForm.estado}
                onChange={(e) => setScoreForm({ ...scoreForm, estado: e.target.value })}
              >
                <option value="programado">Programado</option>
                <option value="en_juego">En Vivo (En Juego)</option>
                <option value="finalizado">Finalizado</option>
              </select>

              {/* Si es finalizado y es empate en partido de eliminación, permitir ganador de penales */}
              {scoreForm.estado === 'finalizado' && 
               selectedPartido.tipo_partido !== 'Regular' && 
               scoreForm.gol_local === scoreForm.gol_visitante && (
                <>
                  <label style={{ display: 'block', marginBottom: '6px', fontWeight: 'bold' }}>Ganador en Penales *</label>
                  <select 
                    className="marcador-select"
                    value={scoreForm.ganador_penales}
                    onChange={(e) => setScoreForm({ ...scoreForm, ganador_penales: e.target.value })}
                    required
                  >
                    <option value="">Seleccione ganador...</option>
                    <option value={selectedPartido.equipo_local}>
                      {getDetallesSeleccion(selectedPartido.equipo_local).pais}
                    </option>
                    <option value={selectedPartido.equipo_visitante}>
                      {getDetallesSeleccion(selectedPartido.equipo_visitante).pais}
                    </option>
                  </select>
                </>
              )}

              <div className="marcador-form-acciones">
                <button type="button" className="marcador-btn-cancelar" onClick={() => setShowScoreModal(false)}>
                  Cancelar
                </button>
                <button type="submit" className="marcador-btn-guardar">
                  Guardar Cambios
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <NotificacionesContainer 
        notificaciones={notificaciones}
        onClose={cerrarNotificacion}
      />
    </div>
  );
};

export default MarcadorPage;
