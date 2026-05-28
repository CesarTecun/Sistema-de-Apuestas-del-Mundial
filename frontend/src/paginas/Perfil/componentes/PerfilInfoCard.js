import React from 'react';
import './PerfilInfoCard.css';

const PerfilInfoCard = ({ user }) => {
  const getInitials = () => {
    if (user?.primer_nombre && user?.primer_apellido) {
      return `${user.primer_nombre[0]}${user.primer_apellido[0]}`.toUpperCase();
    }
    return user?.email?.[0]?.toUpperCase() || 'U';
  };

  return (
    <div className="perfil-info-card">
      <div className="perfil-avatar">
        <span className="avatar-initials">{getInitials()}</span>
      </div>
      <div className="perfil-details">
        <h2 className="perfil-name">
          {user?.primer_nombre} {user?.segundo_nombre} {user?.primer_apellido} {user?.segundo_apellido}
        </h2>
        <p className="perfil-email">{user?.email}</p>
        <div className="perfil-meta">
          <div className="meta-item">
            <span className="meta-label">Teléfono:</span>
            <span className="meta-value">{user?.telefono || 'No registrado'}</span>
          </div>
          <div className="meta-item">
            <span className="meta-label">Fecha de nacimiento:</span>
            <span className="meta-value">
              {user?.fecha_nacimiento 
                ? new Date(user.fecha_nacimiento).toLocaleDateString('es-ES', { 
                    day: '2-digit', 
                    month: '2-digit', 
                    year: 'numeric' 
                  })
                : 'No registrada'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PerfilInfoCard;
