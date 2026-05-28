import React from 'react';
import './PerfilHeader.css';

const PerfilHeader = ({ user }) => {
  return (
    <div className="perfil-header">
      <div className="header-content">
        <h1 className="page-title">Mi Perfil</h1>
        <p className="page-subtitle">Gestiona tu información y estadísticas</p>
      </div>
    </div>
  );
};

export default PerfilHeader;
