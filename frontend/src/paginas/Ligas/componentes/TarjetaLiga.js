import React from 'react';
import './LigasGrid.css';

const TarjetaLiga = ({ liga, onEdit, onDelete, onView, onVerTabla }) => {
  const formatearMonto = (monto) => {
    return new Intl.NumberFormat('es-GT', {
      style: 'currency',
      currency: 'GTQ'
    }).format(monto);
  };

  const isApuesta = liga.tipo_liga?.toLowerCase() === 'apuesta' || liga.tipo_liga?.toLowerCase() === 'dinero' || liga.tipo_liga?.toLowerCase() === 'competitiva';
  const participantes = liga.numero_participantes || liga.participantes || 0;
  const posicion = liga.posicion_usuario || 1;

  return (
    <div className="liga-card-modern">
      <div className="liga-card-header">
        <div className="liga-card-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="2">
            <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path>
            <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path>
            <path d="M4 22h16"></path>
            <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"></path>
            <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"></path>
            <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"></path>
          </svg>
        </div>
        <div className="liga-card-title-group">
          <h3 className="liga-card-title">{liga.nombre_liga}</h3>
          <div className="liga-card-badges">
            {isApuesta ? (
              <span className="liga-badge liga-badge-apuesta">Apuesta</span>
            ) : (
              <span className="liga-badge liga-badge-diversion">Diversión</span>
            )}
          </div>
        </div>
      </div>
      
      <div className="liga-card-body">
        <div className="liga-card-description">
          {isApuesta ? (
            <div className="liga-card-info">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="2">
                <line x1="12" y1="1" x2="12" y2="23"></line>
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
              </svg>
              <span>{formatearMonto(liga.monto_total_recaudado)} - {participantes} participantes</span>
            </div>
          ) : (
            <div className="liga-card-info">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
              <span>Diversión - {participantes} personas</span>
            </div>
          )}
        </div>
      </div>
      
      <div className="liga-card-footer">
        <div className="liga-card-position">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ffd700" strokeWidth="2">
            <circle cx="12" cy="8" r="7"></circle>
            <polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline>
          </svg>
          <span>Posición: {posicion}° lugar</span>
        </div>
        <button 
          className="liga-card-ver-tabla"
          onClick={(e) => {
            e.stopPropagation();
            if (onVerTabla) onVerTabla(liga);
          }}
        >
          Ver Tabla
        </button>
      </div>
      
      <div className="liga-card-actions">
        <button 
          className="action-button view-button"
          onClick={() => onView(liga)}
          title="Ver detalles"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
        </button>
        
        <button 
          className="action-button edit-button"
          onClick={() => onEdit(liga)}
          title="Editar liga"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
        </button>
        
        <button 
          className="action-button delete-button"
          onClick={() => onDelete(liga.id_liga)}
          title="Eliminar liga"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
        </button>
      </div>
    </div>
  );
};

export default TarjetaLiga;
