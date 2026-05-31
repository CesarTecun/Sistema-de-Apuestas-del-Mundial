import React, { useState, useEffect } from 'react';
import servicioLigas from '../../../servicios/servicioLigas';
import './TablaPosicionesLiga.css';

const TablaPosicionesLiga = ({ liga, user, onClose }) => {
  const [participantes, setParticipantes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    cargarParticipantes();
  }, [liga]);

  const cargarParticipantes = async () => {
    setLoading(true);
    const result = await servicioLigas.getParticipantes(liga.liga_id);
    if (result.success) {
      // El backend ya calcula los puntos y ordena por ranking
      setParticipantes(result.data);
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  return (
    <div className="tabla-posiciones-overlay">
      <div className="tabla-posiciones-modal">
        <div className="tabla-posiciones-header">
          <h2>Posiciones - {liga.liga_nombre}</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        {loading && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Cargando participantes...</p>
          </div>
        )}

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {!loading && !error && (
          <div className="tabla-posiciones-content">
            {participantes.length === 0 ? (
              <div className="empty-state">
                <h3>No hay participantes</h3>
                <p>Aún no hay participantes en esta liga.</p>
              </div>
            ) : (
              <table className="posiciones-table">
                <thead>
                  <tr>
                    <th>Posición</th>
                    <th>Usuario</th>
                    <th>Email</th>
                    <th>Estado</th>
                    <th>Puntos</th>
                    <th>Fecha de Unión</th>
                  </tr>
                </thead>
                <tbody>
                  {participantes.map((participante, index) => {
                    const esUsuarioActual = participante.usuario_email === user?.email;
                    return (
                      <tr 
                        key={participante.id_participante}
                        className={esUsuarioActual ? 'mi-participante' : ''}
                      >
                        <td>
                          <span className="posicion-badge">
                            #{index + 1}
                          </span>
                        </td>
                        <td>
                          {participante.usuario_nombre}
                          {esUsuarioActual && (
                            <span className="mi-badge">Yo</span>
                          )}
                        </td>
                        <td>{participante.usuario_email}</td>
                        <td>
                          <span className={`estado-badge ${participante.estado_participacion.toLowerCase()}`}>
                            {participante.estado_participacion}
                          </span>
                        </td>
                        <td>
                          <span className="puntos-badge">
                            {participante.puntos_totales || 0} pts
                          </span>
                        </td>
                        <td>
                          {new Date(participante.fecha_union).toLocaleDateString()}
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

export default TablaPosicionesLiga;
