import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import servicioLigas from '../servicios/servicioLigas';
import './TopBar.css';

const TopBar = ({ user, onLogout, showBackButton = false }) => {
  const navigate = useNavigate();
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
  }, []);

  const handleBack = () => {
    navigate(-1);
  };

  const handleProfileClick = () => {
    navigate('/perfil');
  };

  const invitationCount = invitacionesLoading ? 0 : invitaciones.filter(inv => inv.estado_invitacion === 'Pendiente').length;

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

      <div className="user-info" onClick={handleProfileClick} style={{ cursor: 'pointer' }}>
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
