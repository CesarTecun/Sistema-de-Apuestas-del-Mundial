import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LigasHeader.css';

const LigasHeader = ({ onCreateClick }) => {
  const navigate = useNavigate();

  return (
    <div className="ligas-header">
      <div className="header-content">
        <h1 className="page-title">Ligas del Mundial</h1>
        <p className="page-subtitle">Gestiona las ligas de apuestas</p>
      </div>
      
      <div className="header-actions">
        <button 
          className="partidos-button"
          onClick={() => navigate('/partidos')}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
            <path d="M2 12h20"></path>
          </svg>
          Partidos
        </button>
        <button 
          className="create-button"
          onClick={onCreateClick}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          Nueva Liga
        </button>
      </div>
    </div>
  );
};

export default LigasHeader;
