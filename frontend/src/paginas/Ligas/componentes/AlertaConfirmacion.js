import React from 'react';
import '../../../estilos/componentes/modals.css';

const AlertaConfirmacion = ({ 
  mostrar, 
  titulo, 
  mensaje, 
  onConfirmar, 
  onCancelar,
  textoConfirmar = 'Aceptar',
  textoCancelar = 'Cancelar'
}) => {
  if (!mostrar) return null;

  return (
    <div className="alerta-confirmacion">
      <div className="alerta-confirmacion-content">
        <div className="alerta-confirmacion-icon alerta-confirmacion-icon-danger">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
          </svg>
        </div>
        
        <h3 className="alerta-confirmacion-title">{titulo}</h3>
        <p className="alerta-confirmacion-message">{mensaje}</p>
        
        <div className="alerta-confirmacion-actions">
          <button 
            className="btn btn-secondary"
            onClick={onCancelar}
          >
            {textoCancelar}
          </button>
          <button 
            className="btn btn-primary"
            onClick={onConfirmar}
          >
            {textoConfirmar}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AlertaConfirmacion;
