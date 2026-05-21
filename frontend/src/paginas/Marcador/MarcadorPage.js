import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import { useMarcador } from '../../hooks/useMarcador';
import TopBar from '../Partidos/componentes/TopBar';
import '../../estilos/componentes/modals.css';
import './estilos/MarcadorPage.css';

const Cronometro = ({ partido, onTick }) => {
  const [minuto, setMinuto] = useState(partido.minuto_actual || 0);
  const [periodo, setPeriodo] = useState(partido.periodo_actual || '1T');
  const [tiempoExtra, setTiempoExtra] = useState(partido.tiempo_extra_periodo || 0);
  const [pausado, setPausado] = useState(partido.partido_pausado || false);

  useEffect(() => {
    setMinuto(partido.minuto_actual || 0);
    setPeriodo(partido.periodo_actual || '1T');
    setTiempoExtra(partido.tiempo_extra_periodo || 0);
    setPausado(partido.partido_pausado || false);
  }, [partido]);

  useEffect(() => {
    if (!partido.partido_iniciado || partido.partido_pausado || partido.estado === 'finalizado') {
      return;
    }

    const interval = setInterval(() => {
      setMinuto(prev => {
        const nuevoMinuto = prev + 1;
        if (nuevoMinuto % 1 === 0) {
          onTick?.(nuevoMinuto);
        }
        return nuevoMinuto;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [partido.partido_iniciado, partido.partido_pausado, partido.estado, onTick]);

  const formatoTiempo = () => {
    if (tiempoExtra > 0) {
      return `${minuto}+${tiempoExtra}`;
    }
    return minuto;
  };

  return (
    <div className="cronometro-container">
      <div className="cronometro-time">
        {formatoTiempo()}' {periodo}
      </div>
      {pausado && (
        <div className="cronometro-status paused">⏸️ PAUSADO</div>
      )}
      {!partido.partido_iniciado && partido.estado !== 'finalizado' && (
        <div className="cronometro-status not-started">⏱️ NO INICIADO</div>
      )}
    </div>
  );
};

const MarcadorPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const {
    partidosEnVivo,
    loading,
    error,
    healthStatus,
    cargarPartidosEnVivo,
    actualizarMarcador,
    controlarPartido,
  } = useMarcador();

  const handleLogout = async () => {
    await logout();
    navigate('/home');
  };

  useEffect(() => {
    cargarPartidosEnVivo();
    const interval = setInterval(() => {
      cargarPartidosEnVivo();
    }, 10000);
    return () => clearInterval(interval);
  }, [cargarPartidosEnVivo]);

  const handleActualizarMarcador = async (idPartido, golLocal, golVisitante, faltasLocal, faltasVisitante) => {
    await actualizarMarcador(idPartido, golLocal, golVisitante, 'en_juego', faltasLocal, faltasVisitante);
  };

  const handleIniciarPartido = async (idPartido) => {
    await controlarPartido(idPartido, { partido_iniciado: true });
  };

  const handlePausarPartido = async (idPartido, pausado) => {
    await controlarPartido(idPartido, { partido_pausado: pausado });
  };

  const handleCambiarPeriodo = async (idPartido, nuevoPeriodo) => {
    await controlarPartido(idPartido, { periodo_actual: nuevoPeriodo });
  };

  const handleAgregarTiempoExtra = async (idPartido, minutos) => {
    await controlarPartido(idPartido, { tiempo_extra_periodo: minutos });
  };

  const handleActualizarMinuto = async (idPartido, minuto) => {
    await controlarPartido(idPartido, { minuto_actual: minuto });
  };

  const handleFinalizarPartido = async (idPartido) => {
    await controlarPartido(idPartido, { estado: 'finalizado' });
  };

  if (loading && partidosEnVivo.length === 0) {
    return (
      <div className="marcador-container">
        <div className="marcador-background">
          <div className="marcador-wrapper">
            <div className="loading-container">
              <div className="loading-spinner"></div>
              <p>Cargando marcador...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="marcador-container">
      <div className="marcador-background">
        <div className="marcador-wrapper">
          <TopBar user={user} onLogout={handleLogout} />

          <div className="marcador-content">
            {/* Header del Marcador */}
            <div className="marcador-header">
              <h1>⚽ Marcador en Vivo</h1>
              <div className="health-status">
                {healthStatus ? (
                  <>
                    <span className={healthStatus.success ? 'connected' : 'disconnected'}>
                      {healthStatus.success ? '✅ Conectado' : '❌ Desconectado'}
                    </span>
                    <button
                      onClick={() => cargarPartidosEnVivo()}
                      className="refresh-button"
                    >
                      🔄 Recargar
                    </button>
                  </>
                ) : (
                  <span>Verificando...</span>
                )}
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="error-message">
                <p>{error}</p>
              </div>
            )}

            {/* Lista de partidos en vivo */}
            {partidosEnVivo.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">
                  <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="2" y1="12" x2="22" y2="12"></line>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                  </svg>
                </div>
                <h3>No hay partidos en vivo</h3>
                <p>Los partidos en juego aparecerán aquí automáticamente.</p>
              </div>
            ) : (
              partidosEnVivo.map((partido) => (
                <div key={partido.id_partido} className="partido-card">
                  {/* Encabezado del partido */}
                  <div className="partido-header">
                    <div className="partido-teams">
                      <h3>
                        {partido.equipo_local_detalle?.pais || 'Equipo Local'} vs{' '}
                        {partido.equipo_visitante_detalle?.pais || 'Equipo Visitante'}
                      </h3>
                      <p>Estado: {partido.estado}</p>
                    </div>
                    <div className="partido-score">
                      {partido.gol_local} - {partido.gol_visitante}
                    </div>
                  </div>

                  {/* Cronómetro */}
                  <Cronometro 
                    partido={partido}
                    onTick={(minuto) => handleActualizarMinuto(partido.id_partido, minuto)}
                  />

                  {/* Controles de marcador */}
                  <div className="controls-section">
                    <h4>⚽ Goles</h4>
                    <div className="controls-grid">
                      <button
                        onClick={() => handleActualizarMarcador(partido.id_partido, partido.gol_local + 1, partido.gol_visitante, partido.faltas_local, partido.faltas_visitante)}
                        className="control-button control-button-green"
                      >
                        +1 Local
                      </button>
                      <button
                        onClick={() => handleActualizarMarcador(partido.id_partido, partido.gol_local, partido.gol_visitante + 1, partido.faltas_local, partido.faltas_visitante)}
                        className="control-button control-button-green"
                      >
                        +1 Visitante
                      </button>
                    </div>
                  </div>

                  {/* Controles de faltas */}
                  <div className="controls-section">
                    <h4>🟨 Faltas</h4>
                    <div className="faltas-container">
                      <div className="falta-control">
                        <span>Local: {partido.faltas_local || 0}</span>
                        <button
                          onClick={() => handleActualizarMarcador(partido.id_partido, partido.gol_local, partido.gol_visitante, (partido.faltas_local || 0) + 1, partido.faltas_visitante)}
                          className="control-button control-button-yellow"
                        >
                          +1
                        </button>
                      </div>
                      <div className="falta-control">
                        <span>Visitante: {partido.faltas_visitante || 0}</span>
                        <button
                          onClick={() => handleActualizarMarcador(partido.id_partido, partido.gol_local, partido.gol_visitante, partido.faltas_local, (partido.faltas_visitante || 0) + 1)}
                          className="control-button control-button-yellow"
                        >
                          +1
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Control del partido */}
                  <div className="controls-section">
                    <h4>🎮 Control del Partido</h4>
                    <div className="controls-grid">
                      {!partido.partido_iniciado && (
                        <button
                          onClick={() => handleIniciarPartido(partido.id_partido)}
                          className="control-button control-button-blue"
                        >
                          ▶️ Iniciar
                        </button>
                      )}
                      {partido.partido_iniciado && (
                        <>
                          <button
                            onClick={() => handlePausarPartido(partido.id_partido, !partido.partido_pausado)}
                            className="control-button control-button-orange"
                          >
                            {partido.partido_pausado ? '▶️ Reanudar' : '⏸️ Pausar'}
                          </button>
                          <button
                            onClick={() => handleCambiarPeriodo(partido.id_partido, partido.periodo_actual === '1T' ? '2T' : '1T')}
                            className="control-button control-button-purple"
                          >
                            🔄 Cambiar Período
                          </button>
                          <button
                            onClick={() => handleAgregarTiempoExtra(partido.id_partido, (partido.tiempo_extra_periodo || 0) + 3)}
                            className="control-button control-button-indigo"
                          >
                            +3 min extra
                          </button>
                          <button
                            onClick={() => handleFinalizarPartido(partido.id_partido)}
                            className="control-button control-button-red"
                          >
                            ⏹️ Finalizar
                          </button>
                        </>
                      )}
                    </div>
                  </div>

                  {/* Información del partido */}
                  <div className="partido-info">
                    <div className="partido-info-grid">
                      <div>Período: {partido.periodo_actual || '1T'}</div>
                      <div>Tiempo extra: {partido.tiempo_extra_periodo || 0} min</div>
                      <div>Iniciado: {partido.partido_iniciado ? 'Sí' : 'No'}</div>
                      <div>Pausado: {partido.partido_pausado ? 'Sí' : 'No'}</div>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarcadorPage;
