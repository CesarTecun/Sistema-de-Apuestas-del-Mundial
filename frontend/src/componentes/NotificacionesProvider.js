import React, { createContext, useContext } from 'react';
import useNotificaciones from '../hooks/useNotificaciones';
import NotificacionesContainer from './NotificacionesContainer';
import NotificacionesAxios from './NotificacionesAxios';

const NotificacionesContext = createContext(null);

export const useNotificacionesGlobal = () => {
  const ctx = useContext(NotificacionesContext);
  if (!ctx) {
    throw new Error('useNotificacionesGlobal debe usarse dentro de NotificacionesProvider');
  }
  return ctx;
};

const NotificacionesProvider = ({ children }) => {
  const notificacionesHook = useNotificaciones();

  return (
    <NotificacionesContext.Provider value={notificacionesHook}>
      <NotificacionesAxios />
      {children}
      <NotificacionesContainer
        notificaciones={notificacionesHook.notificaciones}
        onClose={notificacionesHook.cerrarNotificacion}
      />
    </NotificacionesContext.Provider>
  );
};

export default NotificacionesProvider;
