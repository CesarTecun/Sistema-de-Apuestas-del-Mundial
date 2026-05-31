import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import servicioLigas from '../servicios/servicioLigas';
import './TopBar.css';

const TopBar = ({ user, onLogout, showBackButton = false }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [invitaciones, setInvitaciones] = useState([]);
  const [invitacionesLoading, setInvitacionesLoading] = useState(false);

  const cargarInvitaciones = async () => {
    setInvitacionesLoading(true);
    try {
      const result = await servicioLigas.getInvitaciones();
      if (result.success) {
        setInvitaciones(result.data.results || result.data);
      }
    } catch (error) {
      console.error('Error al cargar invitaciones:', error);
    } finally {
      setInvitacionesLoading(false);
    }
  };

  useEffect(() => {
    cargarInvitaciones();
    
    // Actualizar invitaciones cada 30 segundos
    const interval = setInterval(() => {
      cargarInvitaciones();
    }, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const handleBack = () => {
    navigate(-1);
  };

  const handleProfileClick = () => {
    navigate('/perfil');
  };

  const handleNavigate = (path) => {
    navigate(path);
  };

  const invitationCount = invitacionesLoading ? 0 : invitaciones.filter(inv => inv.estado_invitacion === 'Pendiente').length;

  const isActivePath = (path) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  return (
    <div className="top-bar">
      {showBackButton && (
        <div className="top-bar-left">
          <button 
            className="back-button"
            onClick={handleBack}
            aria-label="Volver"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
            <span>Volver</span>
          </button>
        </div>
      )}

      <div className="top-bar-nav">
        <button
          className={`nav-button ${isActivePath('/home') ? 'active' : ''}`}
          onClick={() => handleNavigate('/home')}
          aria-label="Home"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          <span>Home</span>
        </button>
        <button
          className={`nav-button ${isActivePath('/ligas') ? 'active' : ''}`}
          onClick={() => handleNavigate('/ligas')}
          aria-label="Ligas"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          <span>Ligas</span>
        </button>
        <button
          className={`nav-button ${isActivePath('/partidos') ? 'active' : ''}`}
          onClick={() => handleNavigate('/partidos')}
          aria-label="Partidos"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 6v6l4 2"></path>
          </svg>
          <span>Partidos</span>
        </button>
        <button
          className={`nav-button ${isActivePath('/calendario') ? 'active' : ''}`}
          onClick={() => handleNavigate('/calendario')}
          aria-label="Calendario"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
          <span>Calendario</span>
        </button>
        <button
          className={`nav-button ${isActivePath('/selecciones') ? 'active' : ''}`}
          onClick={() => handleNavigate('/selecciones')}
          aria-label="Selecciones"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
          </svg>
          <span>Selecciones</span>
        </button>
        <button
          className={`nav-button ${isActivePath('/pronosticos') ? 'active' : ''}`}
          onClick={() => handleNavigate('/pronosticos')}
          aria-label="Apuestas"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
          </svg>
          <span>Apuestas</span>
        </button>
        {user?.fk_rol === 1 && (
          <button
            className={`nav-button admin-button ${isActivePath('/admin') ? 'active' : ''}`}
            onClick={() => handleNavigate('/admin')}
            aria-label="Admin"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
              <path d="M12 8v4"></path>
              <path d="M12 16h.01"></path>
            </svg>
            <span>Admin</span>
          </button>
        )}
      </div>

      <div className={`user-info ${isActivePath('/perfil') ? 'active' : ''}`} onClick={handleProfileClick} style={{ cursor: 'pointer' }}>
        <div className="user-avatar">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          {invitationCount > 0 && (
            <span className="notification-badge">{invitationCount}</span>
          )}
        </div>
        <div className="user-details">
          <span className="user-name">
            {user?.primer_nombre} {user?.primer_apellido}
          </span>
          <span className="user-email">{user?.email}</span>
        </div>
      </div>
      
      <div className="top-bar-actions">
        <button 
          className="logout-button"
          onClick={onLogout}
          aria-label="Cerrar Sesión"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
        </button>
      </div>
    </div>
  );
};

export default TopBar;
