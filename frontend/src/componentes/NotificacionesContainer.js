import React from 'react';
import Notificacion from '../paginas/Ligas/componentes/Notificacion';
import '../estilos/componentes/modals.css';

const NotificacionesContainer = ({ notificaciones, onClose }) => {
  if (notificaciones.length === 0) {
    return null;
  }

  return (
    <div className="notificaciones-container">
      {notificaciones.map(notificacion => (
        <Notificacion
          key={notificacion.id}
          mensaje={notificacion.mensaje}
          tipo={notificacion.tipo}
          onClose={() => onClose(notificacion.id)}
          autoClose={notificacion.autoClose}
        />
      ))}
    </div>
  );
};

export default NotificacionesContainer;
