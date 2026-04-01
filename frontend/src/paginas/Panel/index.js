import React from 'react';
import { useAuth } from '../../contextos/ContextoAutenticacion';

const PanelPrincipal = () => {
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Bienvenido al Panel Principal</h1>
      
      {user && (
        <div style={{ 
          background: '#f5f5f5', 
          padding: '20px', 
          borderRadius: '8px',
          marginBottom: '20px'
        }}>
          <h2>Información del Usuario</h2>
          <p><strong>ID:</strong> {user.id_usuario}</p>
          <p><strong>Correo:</strong> {user.email}</p>
          <p><strong>Nombre:</strong> {user.primer_nombre} {user.primer_apellido}</p>
          <p><strong>Rol:</strong> {user.fk_rol === 1 ? 'Administrador' : 'Usuario'}</p>
        </div>
      )}

      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        <button 
          onClick={handleLogout}
          style={{
            background: '#ff4d85',
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          Cerrar Sesión
        </button>
      </div>

      <div style={{ marginTop: '30px' }}>
        <h3>Próximas funcionalidades:</h3>
        <ul>
          <li>Ligas y torneos</li>
          <li>Partidos y pronósticos</li>
          <li>Tabla de posiciones</li>
          <li>Premios y recompensas</li>
          <li>Historial de ganadores</li>
        </ul>
      </div>
    </div>
  );
};

export default PanelPrincipal;
