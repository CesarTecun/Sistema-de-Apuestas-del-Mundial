import React, { useState, useEffect } from 'react';
import servicioLigas from '../../../servicios/servicioLigas';
import './TablaPronosticosPartido.css';

const TablaPronosticosPartido = ({ partido, user, onClose }) => {
  const [pronosticos, setPronosticos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Verificar si el partido tiene resultado (finalizado)
  const partidoTieneResultado = () => {
    return partido?.estado_partido?.toLowerCase() === 'finalizado';
  };

  useEffect(() => {
    cargarPronosticosPartido();
  }, [partido]);

  const cargarPronosticosPartido = async () => {
    setLoading(true);
    // Obtener todos los pronósticos de la liga
    const result = await servicioLigas.getParticipantes(partido.fk_id_liga);
    if (result.success) {
      // Filtrar pronósticos por partido (equipo_local y equipo_visitante)
      const pronosticosPartido = result.data.filter(p =>
        p.equipo_local === partido.equipo_local &&
        p.equipo_visitante === partido.equipo_visitante
      );
      // Agrupar por usuario y mostrar su pronóstico para este partido
      const pronosticosAgrupados = pronosticosPartido.reduce((acc, pronostico) => {
        const email = pronostico.usuario_email || pronostico.usuario_nombre;
        if (!acc[email]) {
          acc[email] = {
            usuario_nombre: pronostico.usuario_nombre,
            usuario_email: pronostico.usuario_email,
            resultado_pronosticado: pronostico.resultado_pronosticado,
            puntos_obtenidos: pronostico.puntos_obtenidos || 0,
            tipo_acierto: pronostico.tipo_acierto,
            estado_partido: pronostico.estado_partido
          };
        }
        return acc;
      }, {});

      // Convertir a array y ordenar por puntos de forma descendente
      const pronosticosOrdenados = Object.values(pronosticosAgrupados).sort((a, b) =>
        (b.puntos_obtenidos || 0) - (a.puntos_obtenidos || 0)
      );

      setPronosticos(pronosticosOrdenados);
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  const getBadgeClass = (tipo) => {
    switch (tipo) {
      case 'Marcador exacto': return 'badge-exacto';
      case 'Resultado correcto': return 'badge-correcto';
      case 'Fallido': return 'badge-fallido';
      default: return 'badge-pendiente';
    }
  };

  return (
    <div className="tabla-pronosticos-partido-overlay">
      <div className="tabla-pronosticos-partido-modal">
        <div className="tabla-pronosticos-partido-header">
          <h2>Pronósticos - {partido.equipo_local} vs {partido.equipo_visitante}</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        {loading && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Cargando pronósticos...</p>
          </div>
        )}

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {!loading && !error && (
          <div className="tabla-pronosticos-partido-content">
            {pronosticos.length === 0 ? (
              <div className="empty-state">
                <h3>No hay pronósticos</h3>
                <p>Aún no hay pronósticos registrados para este partido.</p>
              </div>
            ) : (
              <table className="pronosticos-partido-table">
                <thead>
                  <tr>
                    <th>Posición</th>
                    <th>Usuario</th>
                    <th>Email</th>
                    <th>Pronóstico</th>
                    <th>Puntos</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {pronosticos.map((pronostico, index) => {
                    const esUsuarioActual = pronostico.usuario_email === user?.email;
                    const tieneResultado = partidoTieneResultado();
                    return (
                      <tr 
                        key={pronostico.usuario_email} 
                        className={esUsuarioActual ? 'mi-pronostico' : ''}
                      >
                        <td>
                          <span className="posicion-badge">
                            #{index + 1}
                          </span>
                        </td>
                        <td>
                          {pronostico.usuario_nombre}
                          {esUsuarioActual && (
                            <span className="mi-badge">Yo</span>
                          )}
                        </td>
                        <td>{pronostico.usuario_email}</td>
                        <td>
                          {esUsuarioActual || tieneResultado ? (
                            <span className="pronostico-badge">
                              {pronostico.resultado_pronosticado}
                            </span>
                          ) : (
                            <span className="pronostico-oculto">
                              🔒 Oculto
                            </span>
                          )}
                        </td>
                        <td>
                          {esUsuarioActual || tieneResultado ? (
                            <span className="puntos-badge">
                              +{pronostico.puntos_obtenidos} pts
                            </span>
                          ) : (
                            <span className="puntos-oculto">
                              ---
                            </span>
                          )}
                        </td>
                        <td>
                          {esUsuarioActual || tieneResultado ? (
                            <span className={`estado-badge ${getBadgeClass(pronostico.tipo_acierto)}`}>
                              {pronostico.tipo_acierto}
                            </span>
                          ) : (
                            <span className="estado-badge badge-pendiente">
                              Pendiente
                            </span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default TablaPronosticosPartido;
