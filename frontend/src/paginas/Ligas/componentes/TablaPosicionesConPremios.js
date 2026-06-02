import React, { useState, useEffect } from 'react';
import servicioLigas from '../../../servicios/servicioLigas';
import './TablaPosicionesConPremios.css';

const TablaPosicionesConPremios = ({ liga, user, onClose }) => {
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
      // Ordenar por puntos de forma descendente
      const participantesOrdenados = result.data.sort((a, b) =>
        (b.puntos_totales || 0) - (a.puntos_totales || 0)
      );
      setParticipantes(participantesOrdenados);
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  const calcularPremios = (participantesOrdenados, montoTotal) => {
    if (!montoTotal || participantesOrdenados.length === 0) {
      return {};
    }

    // Restar el 5% de la plataforma antes de calcular premios
    const montoParaPremios = montoTotal * 0.95;

    const premios = {};
    const n = participantesOrdenados.length;

    // Identificar empates
    const puntosPorPosicion = participantesOrdenados.map(p => p.puntos_totales || 0);
    const puntosPrimerLugar = puntosPorPosicion[0];
    const puntosSegundoLugar = n > 1 ? puntosPorPosicion[1] : 0;
    const puntosTercerLugar = n > 2 ? puntosPorPosicion[2] : 0;
    const puntosCuartoLugar = n > 3 ? puntosPorPosicion[3] : 0;

    // Contar empates
    const empatePrimerLugar = puntosPorPosicion.filter(p => p === puntosPrimerLugar).length;
    const empateSegundoLugar = n > 1 ? puntosPorPosicion.slice(1).filter(p => p === puntosSegundoLugar).length : 0;
    const empateTercerLugar = n > 2 ? puntosPorPosicion.slice(2).filter(p => p === puntosTercerLugar).length : 0;
    const empateCuartoLugar = n > 3 ? puntosPorPosicion.slice(3).filter(p => p === puntosCuartoLugar).length : 0;

    // Calcular premios según reglas (primeros 4 lugares)
    if (empatePrimerLugar > 1) {
      // Empate en primer lugar: 85% se distribuye equitativamente
      const premioPorGanador = (montoParaPremios * 0.85) / empatePrimerLugar;
      for (let i = 0; i < empatePrimerLugar; i++) {
        premios[participantesOrdenados[i].id_participante] = premioPorGanador;
      }

      // Dar el 10% al tercer lugar (si hay suficientes participantes)
      if (n > 2) {
        if (empateTercerLugar > 1) {
          // Empate en tercer lugar: 10% se reparte equitativamente
          const premioPorGanador = (montoParaPremios * 0.10) / empateTercerLugar;
          for (let i = 2; i < 2 + empateTercerLugar; i++) {
            premios[participantesOrdenados[i].id_participante] = premioPorGanador;
          }
        } else {
          // Tercer lugar: 10%
          premios[participantesOrdenados[2].id_participante] = montoParaPremios * 0.10;
        }
      }
    } else {
      // Primer lugar: 50%
      premios[participantesOrdenados[0].id_participante] = montoParaPremios * 0.50;

      if (n > 1) {
        if (empateSegundoLugar > 1) {
          // Empate en segundo lugar: 35% se reparte equitativamente
          const premioPorGanador = (montoParaPremios * 0.35) / empateSegundoLugar;
          for (let i = 1; i <= empateSegundoLugar; i++) {
            premios[participantesOrdenados[i].id_participante] = premioPorGanador;
          }
        } else {
          // Segundo lugar: 25%
          premios[participantesOrdenados[1].id_participante] = montoParaPremios * 0.25;

          if (n > 2) {
            if (empateTercerLugar > 1) {
              // Empate en tercer lugar: 10% se reparte equitativamente
              const premioPorGanador = (montoParaPremios * 0.10) / empateTercerLugar;
              for (let i = 2; i < 2 + empateTercerLugar; i++) {
                premios[participantesOrdenados[i].id_participante] = premioPorGanador;
              }
            } else {
              // Tercer lugar: 10%
              premios[participantesOrdenados[2].id_participante] = montoParaPremios * 0.10;

              if (n > 3) {
                if (empateCuartoLugar > 1) {
                  // Empate en cuarto lugar: 10% se reparte equitativamente
                  const premioPorGanador = (montoParaPremios * 0.10) / empateCuartoLugar;
                  for (let i = 3; i < 3 + empateCuartoLugar; i++) {
                    premios[participantesOrdenados[i].id_participante] = premioPorGanador;
                  }
                } else {
                  // Cuarto lugar: 10%
                  premios[participantesOrdenados[3].id_participante] = montoParaPremios * 0.10;
                }
              }
            }
          }
        }
      }
    }

    // A partir del 5to lugar, no reciben premio
    return premios;
  };

  const formatearMonto = (monto) => {
    return new Intl.NumberFormat('es-GT', {
      style: 'currency',
      currency: 'GTQ'
    }).format(monto);
  };

  const premios = calcularPremios(participantes, liga.monto_total_recaudado);
  const montoTotal = liga.monto_total_recaudado || 0;

  return (
    <div className="tabla-posiciones-overlay">
      <div className="tabla-posiciones-modal">
        <div className="tabla-posiciones-header">
          <h2>Tabla de Posiciones - {liga.nombre_liga}</h2>
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
                    <th>Puntos</th>
                    <th>Recaudado</th>
                  </tr>
                </thead>
                <tbody>
                  {participantes.map((participante, index) => {
                    const esUsuarioActual = participante.usuario_email === user?.email;
                    const premio = premios[participante.id_participante] || 0;
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
                        <td>
                          <span className="puntos-badge">
                            {participante.puntos_totales || 0} pts
                          </span>
                        </td>
                        <td>
                          <span className="recaudado-badge">
                            {formatearMonto(premio)}
                          </span>
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

export default TablaPosicionesConPremios;
