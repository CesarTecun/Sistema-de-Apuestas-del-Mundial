import React from 'react';

const TarjetaLiga = ({ liga, onEdit, onDelete, onView }) => {
  const formatearMonto = (monto) => {
    return new Intl.NumberFormat('es-GT', {
      style: 'currency',
      currency: 'GTQ'
    }).format(monto);
  };

  const getEstadoColor = (estado) => {
    switch (estado?.toLowerCase()) {
      case 'activa':
        return '#4CAF50';
      case 'inactiva':
        return '#f44336';
      case 'pendiente':
        return '#FF9800';
      default:
        return '#9E9E9E';
    }
  };

  const getTipoLigaIcon = (tipo) => {
    switch (tipo?.toLowerCase()) {
      case 'diversion':
        return '🎮';
      case 'competitiva':
        return '🏆';
      case 'dinero':
        return '💰';
      default:
        return '⚽';
    }
  };

  return (
    <div className="liga-card">
      <div className="liga-header">
        <div className="liga-icon">
          {getTipoLigaIcon(liga.tipo_liga)}
        </div>
        <div className="liga-tipo">
          {liga.tipo_liga || 'Diversion'}
        </div>
        <div 
          className="liga-estado"
          style={{ backgroundColor: getEstadoColor(liga.estado) }}
        >
          {liga.estado || 'Activa'}
        </div>
      </div>
      
      <div className="liga-content">
        <h3 className="liga-nombre">{liga.nombre_liga}</h3>
        
        <div className="liga-info">
          <div className="info-item">
            <div className="info-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
            <span>ID Admin: {liga.fk_administrador || 'Sin asignar'}</span>
          </div>
          
          <div className="info-item">
            <div className="info-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="12" y1="1" x2="12" y2="23"></line>
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
              </svg>
            </div>
            <span>{formatearMonto(liga.monto_total_recaudado)}</span>
          </div>
        </div>
      </div>
      
      <div className="liga-actions">
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
