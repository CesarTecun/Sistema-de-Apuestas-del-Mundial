import React from 'react';
import '../estilos/TarjetaSeleccion.css';

const TarjetaSeleccion = ({ seleccion, onEdit, onDelete }) => {
  return (
    <div className="tarjeta-seleccion">
      <div className="seleccion-header">
        <span className="seleccion-id">#{seleccion.id_seleccion}</span>
        <span className="seleccion-estado activo">Activo</span>
      </div>

      <div className="seleccion-contenido">
        <div className="seleccion-bandera">
          {seleccion.bandera ? (
            <img 
              src={seleccion.bandera} 
              alt={`Bandera de ${seleccion.pais}`}
              className="bandera-img"
            />
          ) : (
            <div className="bandera-placeholder">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="2">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                <path d="M2 12h20"></path>
              </svg>
            </div>
          )}
        </div>

        <div className="seleccion-info">
          <h3 className="seleccion-nombre">{seleccion.pais}</h3>
          {seleccion.fk_id_fase_inicial && (
            <div className="seleccion-meta">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 21h18M5 21V7l8-4 8 4v14M8 21v-2a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
              <span>Fase inicial: {seleccion.fk_id_fase_inicial}</span>
            </div>
          )}
        </div>
      </div>

      <div className="seleccion-acciones">
        <button 
          className="accion-btn editar-btn"
          onClick={() => onEdit(seleccion)}
          title="Editar selección"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
        </button>
        <button 
          className="accion-btn eliminar-btn"
          onClick={() => onDelete(seleccion.id_seleccion)}
          title="Eliminar selección"
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

export default TarjetaSeleccion;
