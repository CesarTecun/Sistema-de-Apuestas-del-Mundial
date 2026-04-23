import React from 'react';
import './LigasModal.css';

const LigasModal = ({ liga, onClose, getEstadoColor }) => {
  if (!liga) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button 
          className="modal-close"
          onClick={onClose}
        >
          ×
        </button>
        
        <div className="modal-header">
          <h2>{liga.nombre_liga}</h2>
          <div className="modal-badges">
            <span className="badge tipo-badge">
              {liga.tipo_liga || 'Diversion'}
            </span>
            <span 
              className="badge estado-badge"
              style={{ backgroundColor: getEstadoColor(liga.estado) }}
            >
              {liga.estado || 'Activa'}
            </span>
          </div>
        </div>
        
        <div className="modal-body">
          <div className="detail-item">
            <label>ID Liga:</label>
            <span>{liga.id_liga}</span>
          </div>
          <div className="detail-item">
            <label>Administrador:</label>
            <span>{liga.fk_administrador || 'Sin asignar'}</span>
          </div>
          <div className="detail-item">
            <label>Monto Recaudado:</label>
            <span>
              {new Intl.NumberFormat('es-GT', {
                style: 'currency',
                currency: 'GTQ'
              }).format(liga.monto_total_recaudado)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LigasModal;
