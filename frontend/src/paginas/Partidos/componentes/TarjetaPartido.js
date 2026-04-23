import React from 'react';
import '../estilos/TarjetaPartido.css';

const TarjetaPartido = ({ partido, selecciones, onEdit, onDelete }) => {
  const getSeleccionNombre = (id) => {
    const seleccion = selecciones.find(s => s.id_seleccion === id);
    return seleccion ? seleccion.pais : `Equipo ${id}`;
  };

  const getSeleccionBandera = (id) => {
    const seleccion = selecciones.find(s => s.id_seleccion === id);
    return seleccion ? seleccion.bandera : null;
  };

  const getEstadoClass = () => {
    if (partido.resultado) return 'jugado';
    const horario = new Date(partido.horario);
    const ahora = new Date();
    if (horario < ahora) return 'en-curso';
    return 'pendiente';
  };

  const formatearFecha = (fechaStr) => {
    const fecha = new Date(fechaStr);
    return fecha.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const estadoClass = getEstadoClass();

  return (
    <div className={`tarjeta-partido ${estadoClass}`}>
      <div className="partido-header">
        <span className={`estado-badge ${estadoClass}`}>
          {partido.resultado ? 'Finalizado' : 'Pendiente'}
        </span>
        <span className="partido-tipo">{partido.tipo_partido}</span>
      </div>

      <div className="partido-equipos">
        <div className="equipo equipo-local">
          {getSeleccionBandera(partido.equipo_local) && (
            <img 
              src={getSeleccionBandera(partido.equipo_local)} 
              alt="Bandera local"
              className="equipo-bandera"
            />
          )}
          <span className="equipo-nombre">
            {getSeleccionNombre(partido.equipo_local)}
          </span>
        </div>

        <div className="partido-marcador">
          {partido.resultado ? (
            <div className="marcador-final">
              <span className="goles">{partido.gol_local}</span>
              <span className="separador">-</span>
              <span className="goles">{partido.gol_visitante}</span>
            </div>
          ) : (
            <div className="marcador-pendiente">VS</div>
          )}
        </div>

        <div className="equipo equipo-visitante">
          <span className="equipo-nombre">
            {getSeleccionNombre(partido.equipo_visitante)}
          </span>
          {getSeleccionBandera(partido.equipo_visitante) && (
            <img 
              src={getSeleccionBandera(partido.equipo_visitante)} 
              alt="Bandera visitante"
              className="equipo-bandera"
            />
          )}
        </div>
      </div>

      <div className="partido-info">
        <div className="info-item">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          <span>{formatearFecha(partido.horario)}</span>
        </div>
      </div>

      <div className="partido-acciones">
        <button 
          className="accion-btn editar-btn"
          onClick={() => onEdit(partido)}
          title="Editar partido"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
        </button>
        <button 
          className="accion-btn eliminar-btn"
          onClick={() => onDelete(partido.id_partido)}
          title="Eliminar partido"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
        </button>
      </div>
    </div>
  );
};

export default TarjetaPartido;
