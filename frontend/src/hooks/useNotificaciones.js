import { useState, useCallback } from 'react';

const useNotificaciones = () => {
  const [notificaciones, setNotificaciones] = useState([]);

  const mostrarNotificacion = useCallback((mensaje, tipo = 'info', autoClose = true) => {
    const id = Date.now() + Math.random();
    const nuevaNotificacion = {
      id,
      mensaje,
      tipo,
      autoClose
    };

    setNotificaciones(prev => [...prev, nuevaNotificacion]);

    return id;
  }, []);

  const cerrarNotificacion = useCallback((id) => {
    setNotificaciones(prev => 
      prev.filter(notificacion => notificacion.id !== id)
    );
  }, []);

  const limpiarNotificaciones = useCallback(() => {
    setNotificaciones([]);
  }, []);

  // Métodos de conveniencia
  const success = useCallback((mensaje, autoClose) => 
    mostrarNotificacion(mensaje, 'success', autoClose), [mostrarNotificacion]);
  
  const error = useCallback((mensaje, autoClose) => 
    mostrarNotificacion(mensaje, 'error', autoClose), [mostrarNotificacion]);
  
  const warning = useCallback((mensaje, autoClose) => 
    mostrarNotificacion(mensaje, 'warning', autoClose), [mostrarNotificacion]);
  
  const info = useCallback((mensaje, autoClose) => 
    mostrarNotificacion(mensaje, 'info', autoClose), [mostrarNotificacion]);

  return {
    notificaciones,
    mostrarNotificacion,
    cerrarNotificacion,
    limpiarNotificaciones,
    success,
    error,
    warning,
    info
  };
};

export default useNotificaciones;
