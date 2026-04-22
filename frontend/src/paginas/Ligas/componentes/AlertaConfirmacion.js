import React from 'react';

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
    <div className="alerta-overlay">
      <div className="alerta-contenido">
        <div className="alerta-icono">
          <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#EC4899" strokeWidth="2">
            <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
          </svg>
        </div>
        
        <h3 className="alerta-titulo">{titulo}</h3>
        <p className="alerta-mensaje">{mensaje}</p>
        
        <div className="alerta-botones">
          <button 
            className="alerta-boton alerta-cancelar"
            onClick={onCancelar}
          >
            {textoCancelar}
          </button>
          <button 
            className="alerta-boton alerta-confirmar"
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
