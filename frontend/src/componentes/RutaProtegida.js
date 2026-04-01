import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contextos/ContextoAutenticacion';

const RutaProtegida = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh' 
      }}>
        <div>Cargando...</div>
      </div>
    );
  }

  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

export default RutaProtegida;
