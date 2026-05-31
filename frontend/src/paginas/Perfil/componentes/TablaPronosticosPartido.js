import React, { useState, useEffect } from 'react';
import servicioLigas from '../../../servicios/servicioLigas';
import servicioPronosticos from '../../../servicios/servicioPronosticos';
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
    try {
      console.log('[TablaPronosticosPartido] Cargando pronósticos para partido:', partido.fk_id_partido, 'liga:', partido.fk_id_liga);

      // Obtener pronósticos del partido filtrados por liga
      let pronosticosResult;
      if (partido.fk_id_liga) {
        pronosticosResult = await servicioPronosticos.getPronosticosPorPartidoLiga(
          partido.fk_id_partido,
          partido.fk_id_liga
        );
        console.log('[TablaPronosticosPartido] Resultado endpoint por-partido-liga:', pronosticosResult);

        // Fallback al endpoint original si el nuevo endpoint no está disponible (404 u otro error)
        if (!pronosticosResult.success) {
          console.warn('[TablaPronosticosPartido] Endpoint por-partido-liga falló, usando fallback. Error:', pronosticosResult.error);
          pronosticosResult = await servicioPronosticos.getPronosticosPorPartido(partido.fk_id_partido);
          console.log('[TablaPronosticosPartido] Resultado fallback:', pronosticosResult);
        }
      } else {
        pronosticosResult = await servicioPronosticos.getPronosticosPorPartido(partido.fk_id_partido);
        console.log('[TablaPronosticosPartido] Resultado endpoint por-partido (sin liga):', pronosticosResult);
      }

      if (pronosticosResult.success) {
        console.log('[TablaPronosticosPartido] Pronósticos cargados:', pronosticosResult.data.length);

        // Ordenar por puntos de forma descendente
        const pronosticosOrdenados = pronosticosResult.data.sort((a, b) =>
          (b.puntos_obtenidos || 0) - (a.puntos_obtenidos || 0)
        );

        setPronosticos(pronosticosOrdenados);
      } else {
        console.error('[TablaPronosticosPartido] Error al cargar pronósticos:', pronosticosResult.error);
        setError(pronosticosResult.error);
      }
    } catch (err) {
      console.error('[TablaPronosticosPartido] Excepción al cargar pronósticos:', err);
      setError('Error al cargar pronósticos');
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
                        key={`${pronostico.usuario_email}-${index}`}
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
                        <td>
                          {esUsuarioActual || tieneResultado ? (
                            <span className="pronostico-badge">
                              {pronostico.resultado_display}
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
                            <span className={`estado-badge badge-pendiente`}>
                              {pronostico.ganador_pronostico}
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
