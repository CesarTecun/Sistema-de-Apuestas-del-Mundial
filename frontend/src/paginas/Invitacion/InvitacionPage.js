import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './InvitacionPage.css';

const InvitacionPage = () => {
  const { codigo } = useParams();
  const navigate = useNavigate();
  const [invitacion, setInvitacion] = useState(null);
  const [liga, setLiga] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [email, setEmail] = useState('');
  const [registrando, setRegistrando] = useState(false);

  useEffect(() => {
    cargarInvitacion();
  }, [codigo]);

  const cargarInvitacion = async () => {
    try {
      const response = await axios.get(`https://apuestas-del-mundial.onrender.com/api/ligas/invitaciones/publico/${codigo}/`);
      setInvitacion(response.data);
      setLiga(response.data.liga);
      if (response.data.email_invitado) {
        setEmail(response.data.email_invitado);
      }
    } catch (err) {
      setError('No se pudo cargar la invitación. Es posible que haya expirado o no sea válida.');
    } finally {
      setLoading(false);
    }
  };

  const handleAceptar = async () => {
    if (!email) {
      setError('Por favor ingresa tu correo electrónico');
      return;
    }

    setRegistrando(true);
    try {
      const response = await axios.post(`https://apuestas-del-mundial.onrender.com/api/ligas/invitaciones/publico/${codigo}/`, { email });
      
      // Si el usuario fue creado automáticamente, guardar el token
      if (response.data.access) {
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
      }
      
      alert('¡Invitación aceptada exitosamente! Ya eres parte de la liga.');
      navigate('/home');
    } catch (err) {
      setError(err.response?.data?.error || 'Error al aceptar la invitación');
    } finally {
      setRegistrando(false);
    }
  };

  if (loading) {
    return (
      <div className="invitacion-container">
        <div className="invitacion-card">
          <div className="loading-spinner"></div>
          <p>Cargando invitación...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="invitacion-container">
        <div className="invitacion-card error">
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={() => navigate('/login')}>Ir al inicio de sesión</button>
        </div>
      </div>
    );
  }

  if (!invitacion) {
    return (
      <div className="invitacion-container">
        <div className="invitacion-card error">
          <h2>Invitación no encontrada</h2>
          <button onClick={() => navigate('/login')}>Ir al inicio de sesión</button>
        </div>
      </div>
    );
  }

  if (invitacion.estado !== 'Pendiente') {
    return (
      <div className="invitacion-container">
        <div className="invitacion-card">
          <h2>Invitación {invitacion.estado}</h2>
          <p>Esta invitación ya fue {invitacion.estado.toLowerCase()}.</p>
          <button onClick={() => navigate('/login')}>Ir al inicio de sesión</button>
        </div>
      </div>
    );
  }

  return (
    <div className="invitacion-container">
      <div className="invitacion-card">
        <div className="invitacion-header">
          <h1>¡Has sido invitado a una liga!</h1>
        </div>
        
        {liga && (
          <div className="invitacion-liga-info">
            <h2>{liga.nombre_liga}</h2>
            <p className="liga-tipo">Tipo: {liga.tipo_liga}</p>
            {liga.descripcion && <p className="liga-descripcion">{liga.descripcion}</p>}
          </div>
        )}

        <div className="invitacion-form">
          <label htmlFor="email">Correo electrónico:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="tu@email.com"
            required
          />
          
          <button 
            className="btn-aceptar" 
            onClick={handleAceptar}
            disabled={registrando}
          >
            {registrando ? 'Procesando...' : 'Aceptar Invitación'}
          </button>
          
          <button 
            className="btn-cancelar" 
            onClick={() => navigate('/login')}
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>
  );
};

export default InvitacionPage;
