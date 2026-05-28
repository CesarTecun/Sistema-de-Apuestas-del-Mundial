import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import { servicioPartidos } from '../../servicios/servicioPartidos';
import { servicioSelecciones } from '../../servicios/servicioSelecciones';
import TopBar from './componentes/TopBar';
import useNotificaciones from '../../hooks/useNotificaciones';
import NotificacionesContainer from '../../componentes/NotificacionesContainer';
import './estilos/JugadoresSeleccionPage.css';

const JugadoresSeleccionPage = () => {
  const { id_seleccion } = useParams();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { notificaciones, cerrarNotificacion, error: mostrarError } = useNotificaciones();

  const [seleccion, setSeleccion] = useState(null);
  const [jugadores, setJugadores] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const cargarDatos = async () => {
      setLoading(true);
      const [resSeleccion, resJugadores] = await Promise.all([
        servicioSelecciones.getSeleccion(id_seleccion),
        servicioPartidos.getJugadoresPorSeleccion(id_seleccion),
      ]);

      if (resSeleccion.success) {
        setSeleccion(resSeleccion.data);
      } else {
        mostrarError(resSeleccion.error || 'Error al cargar la selección');
      }

      if (resJugadores.success) {
        setJugadores(resJugadores.data);
      } else {
        mostrarError(resJugadores.error || 'Error al cargar los jugadores');
      }

      setLoading(false);
    };

    cargarDatos();
  }, [id_seleccion, mostrarError]);

  const handleLogout = async () => {
    await logout();
    navigate('/home');
  };

  const calcularEdad = (fechaNacimiento) => {
    if (!fechaNacimiento) return null;
    const hoy = new Date();
    const nac = new Date(fechaNacimiento);
    let edad = hoy.getFullYear() - nac.getFullYear();
    const mes = hoy.getMonth() - nac.getMonth();
    if (mes < 0 || (mes === 0 && hoy.getDate() < nac.getDate())) {
      edad--;
    }
    return edad;
  };

  return (
    <div className="jugadores-container">
      <div className="jugadores-background">
        <div className="jugadores-wrapper">
          <TopBar user={user} onLogout={handleLogout} />

          <div className="jugadores-content">
            <button
              className="back-button"
              onClick={() => navigate('/selecciones')}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="15 18 9 12 15 6"></polyline>
              </svg>
              <span>Volver a Selecciones</span>
            </button>

            {loading ? (
              <div className="loading-container">
                <div className="loading-spinner"></div>
                <p>Cargando jugadores...</p>
              </div>
            ) : (
              <>
                {seleccion && (
                  <div className="seleccion-header-detail">
                    {seleccion.bandera && (
                      <img
                        src={seleccion.bandera}
                        alt={`Bandera de ${seleccion.pais}`}
                        className="seleccion-bandera-detail"
                      />
                    )}
                    <h1 className="seleccion-titulo">{seleccion.pais}</h1>
                    <p className="seleccion-subtitulo">
                      {jugadores.length} jugador{jugadores.length !== 1 ? 'es' : ''} registrados
                    </p>
                  </div>
                )}

                {jugadores.length === 0 ? (
                  <div className="empty-state">
                    <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                      <circle cx="9" cy="7" r="4"></circle>
                      <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                      <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                    </svg>
                    <h3>No hay jugadores registrados</h3>
                    <p>Esta selección aún no tiene jugadores en el sistema.</p>
                  </div>
                ) : (
                  <div className="jugadores-grid">
                    {jugadores.map((jugador) => (
                      <div key={jugador.id_jugador} className="jugador-card">
                        <div className="jugador-avatar">
                          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="1.5">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                            <circle cx="12" cy="7" r="4"></circle>
                          </svg>
                        </div>
                        <div className="jugador-info">
                          <h4 className="jugador-nombre">
                            {jugador.primer_nombre} {jugador.primer_apellido}
                          </h4>
                          <div className="jugador-meta">
                            {jugador.dorsal && (
                              <span className="jugador-dorsal">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                                </svg>
                                #{jugador.dorsal}
                              </span>
                            )}
                            {jugador.posicion && (
                              <span className="jugador-posicion">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                  <circle cx="12" cy="12" r="10"></circle>
                                  <line x1="2" y1="12" x2="22" y2="12"></line>
                                </svg>
                                {jugador.posicion}
                              </span>
                            )}
                            {calcularEdad(jugador.fecha_nacimiento) && (
                              <span className="jugador-edad">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                  <circle cx="12" cy="12" r="10"></circle>
                                  <polyline points="12 6 12 12 16 14"></polyline>
                                </svg>
                                {calcularEdad(jugador.fecha_nacimiento)} años
                              </span>
                            )}
                          </div>
                          <p className="jugador-nombre-completo">
                            {[jugador.primer_nombre, jugador.segundo_nombre, jugador.primer_apellido, jugador.segundo_apellido]
                              .filter(Boolean)
                              .join(' ')}
                          </p>
                        </div>
                      </div>
                    ))}
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

export default JugadoresSeleccionPage;
