import React, { useState, useEffect } from 'react';
import servicioLigas from '../../../servicios/servicioLigas';
import './TablaParticipantes.css';

const TablaParticipantes = ({ liga, onClose }) => {
  const [participantes, setParticipantes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    cargarParticipantes();
  }, [liga]);

  const cargarParticipantes = async () => {
    setLoading(true);
    const result = await servicioLigas.getParticipantes(liga.id_liga);
    if (result.success) {
      // Agrupar por usuario (email) y sumar puntos
      const participantesAgrupados = result.data.reduce((acc, participante) => {
        const email = participante.usuario_email || participante.usuario_nombre;
        if (!acc[email]) {
          acc[email] = {
            ...participante,
            puntos_totales: 0
          };
        }
        acc[email].puntos_totales += (participante.puntos_totales || 0);
        return acc;
      }, {});

      // Convertir a array y ordenar por puntos de forma descendente
      const participantesOrdenados = Object.values(participantesAgrupados).sort((a, b) =>
        (b.puntos_totales || 0) - (a.puntos_totales || 0)
      );

      setParticipantes(participantesOrdenados);
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  return (
    <div className="tabla-participantes-overlay">
      <div className="tabla-participantes-modal">
        <div className="tabla-participantes-header">
          <h2>Participantes de {liga.nombre_liga}</h2>
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
          <div className="tabla-participantes-content">
            {participantes.length === 0 ? (
              <div className="empty-state">
                <h3>No hay participantes</h3>
                <p>Aún no hay participantes en esta liga.</p>
              </div>
            ) : (
              <table className="participantes-table">
                <thead>
                  <tr>
                    <th>Usuario</th>
                    <th>Email</th>
                    <th>Estado</th>
                    <th>Fecha de Unión</th>
                  </tr>
                </thead>
                <tbody>
                  {participantes.map((participante) => (
                    <tr key={participante.id_participante}>
                      <td>{participante.usuario_nombre}</td>
                      <td>{participante.usuario_email}</td>
                      <td>
                        <span className={`estado-badge ${participante.estado_participacion.toLowerCase()}`}>
                          {participante.estado_participacion}
                        </span>
                      </td>
                      <td>
                        {new Date(participante.fecha_union).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default TablaParticipantes;
