import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import servicioPronosticos from '../../servicios/servicioPronosticos';
import servicioLigas from '../../servicios/servicioLigas';
import servicioPartidos from '../../servicios/servicioPartidos';
import TopBar from '../../componentes/TopBar';
import './estilos/PronosticosPage.css';

const PronosticosPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [ligas, setLigas] = useState([]);
  const [selectedLiga, setSelectedLiga] = useState(null);
  const [partidos, setPartidos] = useState([]);
  const [pronosticos, setPronosticos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selecciones, setSelecciones] = useState([]);
  const [filtroPronostico, setFiltroPronostico] = useState('todos');

  useEffect(() => {
    cargarLigas();
    cargarSelecciones();
  }, []);

  useEffect(() => {
    if (selectedLiga) {
      cargarPartidosDeLiga(selectedLiga);
      cargarPronosticosDeLiga(selectedLiga);
    }
  }, [selectedLiga]);

  const cargarLigas = async () => {
    setLoading(true);
    const result = await servicioLigas.getLigas();
    if (result.success) {
      setLigas(result.data);
      if (result.data.length > 0) {
        setSelectedLiga(result.data[0].id_liga);
      }
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  const cargarSelecciones = async () => {
    const result = await servicioPartidos.getSelecciones();
    if (result.success) {
      setSelecciones(result.data);
    }
  };

  const cargarPartidosDeLiga = async (ligaId) => {
    const result = await servicioPartidos.getPartidosPorLiga(ligaId);
    if (result.success) {
      setPartidos(result.data);
    }
  };

  const cargarPronosticosDeLiga = async (ligaId) => {
    const result = await servicioPronosticos.getPronosticosPorLiga(ligaId);
    if (result.success) {
      setPronosticos(result.data);
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

  const getPronosticoUsuario = (partidoId) => {
    return pronosticos.find(p => p.fk_id_partido === partidoId && p.fk_id_usuario === user?.id_usuario);
  };

  const partidosFiltrados = partidos.filter((partido) => {
    const pronostico = getPronosticoUsuario(partido.id_partido);
    if (filtroPronostico === 'todos') return true;
    if (filtroPronostico === 'pronosticados') return !!pronostico;
    if (filtroPronostico === 'no-pronosticados') return !pronostico;
    return true;
  });

  const handleCrearPronostico = async (partidoId, golLocal, golVisitante) => {
    if (!selectedLiga) return;
    
    const result = await servicioPronosticos.crearPronostico({
      fk_id_usuario: user.id_usuario,
      fk_id_partido: partidoId,
      fk_id_liga: selectedLiga,
      gol_local: golLocal,
      gol_visitante: golVisitante,
    });

    if (result.success) {
      cargarPronosticosDeLiga(selectedLiga);
    } else {
      setError(result.error);
    }
  };

  const handleEliminarPronostico = async (pronosticoId) => {
    const result = await servicioPronosticos.eliminarPronostico(pronosticoId);
    if (result.success) {
      cargarPronosticosDeLiga(selectedLiga);
    } else {
      setError(result.error);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/home');
  };

  if (loading) {
    return (
      <div className="pronosticos-container">
        <div className="pronosticos-background">
          <div className="pronosticos-wrapper">
            <TopBar user={user} onLogout={handleLogout} showBackButton={true} />
            <div className="loading-container">
              <div className="loading-spinner"></div>
              <p>Cargando pronósticos...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="pronosticos-container">
      <div className="pronosticos-background">
        <div className="pronosticos-wrapper">
          <TopBar user={user} onLogout={handleLogout} showBackButton={true} />

          <div className="pronosticos-content">
            {/* Header */}
            <div className="pronosticos-header">
              <h1>Pronósticos</h1>
              <div className="liga-selector">
                <label>Liga:</label>
                <select
                  value={selectedLiga || ''}
                  onChange={(e) => setSelectedLiga(Number(e.target.value))}
                >
                  {ligas.map((liga) => (
                    <option key={liga.id_liga} value={liga.id_liga}>
                      {liga.nombre_liga}
                    </option>
                  ))}
                </select>
                <label>Filtrar por:</label>
                <select
                  value={filtroPronostico}
                  onChange={(e) => setFiltroPronostico(e.target.value)}
                >
                  <option value="todos">Todos</option>
                  <option value="pronosticados">Pronosticados</option>
                  <option value="no-pronosticados">No pronosticados</option>
                </select>
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="error-message">
                <p>{error}</p>
                <button onClick={() => setError(null)} className="dismiss-error">×</button>
              </div>
            )}

            {/* Lista de partidos */}
            <div className="partidos-list">
              {partidosFiltrados.length === 0 ? (
                <div className="empty-state">
                  <h3>No hay partidos disponibles</h3>
                  <p>Selecciona una liga para ver los partidos disponibles.</p>
                </div>
              ) : (
                partidosFiltrados.map((partido) => {
                  const pronostico = getPronosticoUsuario(partido.id_partido);
                  const puedePronosticar = !pronostico && partido.estado_partido !== 'finalizado';
                  
                  return (
                    <div key={partido.id_partido} className="partido-card">
                      <div className="partido-info">
                        <div className="equipos">
                          {getSeleccionBandera(partido.equipo_local) && (
                            <img
                              src={getSeleccionBandera(partido.equipo_local)}
                              alt=""
                              className="bandera"
                            />
                          )}
                          <span className="equipo-nombre">{getSeleccionNombre(partido.equipo_local)}</span>
                          <span className="vs">vs</span>
                          <span className="equipo-nombre">{getSeleccionNombre(partido.equipo_visitante)}</span>
                          {getSeleccionBandera(partido.equipo_visitante) && (
                            <img
                              src={getSeleccionBandera(partido.equipo_visitante)}
                              alt=""
                              className="bandera"
                            />
                          )}
                        </div>
                        <div className="partido-estado">
                          Estado: {partido.estado_partido}
                        </div>
                      </div>

                      {pronostico ? (
                        <div className="pronostico-existente">
                          <div className="pronostico-info">
                            <span>Tu pronóstico: </span>
                            <strong>{pronostico.gol_local} - {pronostico.gol_visitante}</strong>
                            {pronostico.puntos_obtenidos > 0 && (
                              <span className="puntos-badge">+{pronostico.puntos_obtenidos} pts</span>
                            )}
                          </div>
                          {partido.estado_partido !== 'finalizado' && (
                            <div className="pronostico-acciones">
                              <button
                                onClick={() => handleEliminarPronostico(pronostico.id_pronostico)}
                                className="btn-eliminar"
                              >
                                Eliminar
                              </button>
                            </div>
                          )}
                        </div>
                      ) : puedePronosticar ? (
                        <div className="pronostico-form">
                          <div className="input-group">
                            <label>Goles {getSeleccionNombre(partido.equipo_local)}:</label>
                            <input
                              type="number"
                              min="0"
                              defaultValue={0}
                              id={`gol-local-${partido.id_partido}`}
                            />
                          </div>
                          <div className="input-group">
                            <label>Goles {getSeleccionNombre(partido.equipo_visitante)}:</label>
                            <input
                              type="number"
                              min="0"
                              defaultValue={0}
                              id={`gol-visitante-${partido.id_partido}`}
                            />
                          </div>
                          <button
                            onClick={() => {
                              const golLocal = document.getElementById(`gol-local-${partido.id_partido}`).value;
                              const golVisitante = document.getElementById(`gol-visitante-${partido.id_partido}`).value;
                              handleCrearPronostico(partido.id_partido, Number(golLocal), Number(golVisitante));
                            }}
                            className="btn-enviar"
                          >
                            Enviar Pronóstico
                          </button>
                        </div>
                      ) : (
                        <div className="pronostico-cerrado">
                          {partido.estado === 'finalizado' ? 'Partido finalizado' : 'Ventana de pronósticos cerrada'}
                        </div>
                      )}
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PronosticosPage;
