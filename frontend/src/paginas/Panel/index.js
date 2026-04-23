import React from 'react';

import { useNavigate } from 'react-router-dom';

import { useAuth } from '../../contextos/ContextoAutenticacion';



const PanelPrincipal = () => {

  const { user, logout } = useAuth();

  const navigate = useNavigate();



  const handleLogout = async () => {

    await logout();

  };



  const goToLigas = () => {

    navigate('/ligas');

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



      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginBottom: '30px' }}>

        <button 

          onClick={goToLigas}

          style={{

            background: '#a83279',

            color: 'white',

            border: 'none',

            padding: '12px 24px',

            borderRadius: '5px',

            cursor: 'pointer',

            fontSize: '16px',

            fontWeight: '600'

          }}

        >

          🏆 Gestionar Ligas

        </button>

        

        <button 

          onClick={handleLogout}

          style={{

            background: '#ff4d85',

            color: 'white',

            border: 'none',

            padding: '12px 24px',

            borderRadius: '5px',

            cursor: 'pointer',

            fontSize: '16px'

          }}

        >

          Cerrar Sesión

        </button>

      </div>



      <div style={{ marginTop: '30px' }}>

        <h3>Funcionalidades Disponibles:</h3>

        <ul>

          <li>✅ <strong>Ligas y torneos</strong> - Gestiona las ligas de apuestas</li>

          <li>🔄 Partidos y pronósticos (próximamente)</li>

          <li>📊 Tabla de posiciones (próximamente)</li>

          <li>🏆 Premios y recompensas (próximamente)</li>

          <li>📈 Historial de ganadores (próximamente)</li>

        </ul>

      </div>

    </div>

  );

};



export default PanelPrincipal;

