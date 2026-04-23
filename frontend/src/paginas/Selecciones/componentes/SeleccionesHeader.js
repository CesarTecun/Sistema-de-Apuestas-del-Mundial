import React from 'react';
import '../estilos/SeleccionesHeader.css';

const SeleccionesHeader = ({ onCreateClick }) => {
  return (
    <div className="selecciones-header">
      <div className="header-content">
        <h1 className="page-title">Selecciones del Mundial</h1>
        <p className="page-subtitle">Gestiona las selecciones participantes</p>
      </div>
      
      <button 
        className="create-button"
        onClick={onCreateClick}
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        Nueva Selección
      </button>
    </div>
  );
};

export default SeleccionesHeader;
