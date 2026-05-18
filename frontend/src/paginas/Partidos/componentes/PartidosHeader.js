import React from 'react';
import '../estilos/PartidosHeader.css';

const PartidosHeader = ({ onCreateClick, ligas, selectedLigaId, onLigaChange, canManageSelectedLiga, requireAdminSelection }) => {
  const disabledCreate = !selectedLigaId || !canManageSelectedLiga;

  return (
    <div className="partidos-header">
      <div className="header-content">
        <h1 className="page-title">Partidos del Mundial</h1>
        <p className="page-subtitle">Gestiona los partidos del torneo</p>
        {ligas?.length > 0 && (
          <div className="header-selectors">
            <label className="selector-label" htmlFor="filtro-liga">
              Filtrar por liga
            </label>
            <select
              id="filtro-liga"
              value={selectedLigaId || ''}
              onChange={(e) => onLigaChange(e.target.value)}
            >
              <option value="">Todas mis ligas</option>
              {ligas.map((liga) => (
                <option key={liga.id_liga} value={liga.id_liga}>
                  {liga.nombre_liga}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>
      
      <button 
        className={`create-button ${disabledCreate ? 'disabled' : ''}`}
        onClick={onCreateClick}
        disabled={disabledCreate}
        title={disabledCreate ? (requireAdminSelection ? 'Selecciona una liga que administres para crear partidos' : 'Selecciona una liga para crear partidos') : 'Crear partido'}
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        Nuevo Partido
      </button>
    </div>
  );
};

export default PartidosHeader;
