import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import TarjetaLiga from './componentes/TarjetaLiga';
import FormularioLiga from './componentes/FormularioLiga';
import TopBar from './componentes/TopBar';
import LigasHeader from './componentes/LigasHeader';
import SearchBar from './componentes/SearchBar';
import LigasModal from './componentes/LigasModal';
import useNotificaciones from '../../hooks/useNotificaciones';
import { useLigas } from '../../hooks/useLigas';
import NotificacionesContainer from '../../componentes/NotificacionesContainer';
import AlertaConfirmacion from './componentes/AlertaConfirmacion';
import '../../estilos/componentes/modals.css';
import './estilos/LigasPage.css';

const LigasPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { 
    notificaciones, 
    cerrarNotificacion, 
    success, 
    error: mostrarError
  } = useNotificaciones();
  
  const {
    loading,
    error,
    searchTerm,
    setSearchTerm,
    filteredLigas,
    createLiga,
    updateLiga,
    deleteLiga
  } = useLigas();

  const [showForm, setShowForm] = useState(false);
  const [editingLiga, setEditingLiga] = useState(null);
  const [viewingLiga, setViewingLiga] = useState(null);
  const [alertaConfirmacion, setAlertaConfirmacion] = useState({
    mostrar: false,
    paso: 1,
    ligaId: null
  });
  const [hasVisited, setHasVisited] = useState(false);

  useEffect(() => {
    const visited = sessionStorage.getItem('ligas_visited');
    if (visited) {
      setHasVisited(true);
    } else {
      sessionStorage.setItem('ligas_visited', 'true');
    }
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate('/home');
  };

  const handleFormSubmit = async (formData) => {
    const result = editingLiga 
      ? await updateLiga(editingLiga.id_liga, formData)
      : await createLiga(formData);
    
    if (result.success) {
      setShowForm(false);
      setEditingLiga(null);
      success(editingLiga ? '¡Liga actualizada exitosamente!' : '¡Liga creada exitosamente!');
    } else {
      mostrarError(result.error || 'Error al procesar la operación');
    }
  };

  const handleFormCancel = () => {
    const scrollPosition = window.scrollY || document.documentElement.scrollTop;
    setShowForm(false);
    setEditingLiga(null);
    setTimeout(() => {
      window.scrollTo(0, scrollPosition);
    }, 50);
  };

  const handleEditClick = (liga) => {
    setEditingLiga(liga);
    setShowForm(true);
  };

  const handleCreateClick = () => {
    setEditingLiga(null);
    setShowForm(true);
  };

  const handleDeleteLiga = (ligaId) => {
    setAlertaConfirmacion({
      mostrar: true,
      paso: 1,
      ligaId: ligaId
    });
  };

  const confirmarEliminacion = async () => {
    if (alertaConfirmacion.paso === 1) {
      setAlertaConfirmacion({
        ...alertaConfirmacion,
        paso: 2
      });
    } else {
      const result = await deleteLiga(alertaConfirmacion.ligaId);
      if (result.success) {
        success('Liga eliminada exitosamente');
      } else {
        mostrarError(result.error || 'Error al eliminar liga');
      }
      setAlertaConfirmacion({ mostrar: false, paso: 1, ligaId: null });
    }
  };

  const cancelarEliminacion = () => {
    setAlertaConfirmacion({ mostrar: false, paso: 1, ligaId: null });
  };

  const handleViewLiga = (liga) => {
    setViewingLiga(liga);
  };

  const handleVerTabla = (liga) => {
    console.log('Navegando a tabla de posiciones para liga:', liga.id_liga);
  };

  const getEstadoColor = (estado) => {
    switch (estado?.toLowerCase()) {
      case 'activa':
        return '#4CAF50';
      case 'inactiva':
        return '#f44336';
      case 'pendiente':
        return '#FF9800';
      default:
        return '#9E9E9E';
    }
  };

  if (showForm) {
    return (
      <div className="ligas-container">
        <div className="ligas-background">
          <div className="ligas-form-container">
            <div className="logo-container">
              <div className="logo">
                <svg width="100" height="100" viewBox="0 0 100 100" fill="none">
                  <circle cx="50" cy="50" r="45" fill="url(#gradient)" opacity="0.9"/>
                  <path d="M30 35 L70 35 L70 65 L30 65 Z" fill="white" opacity="0.9"/>
                  <path d="M40 45 L60 45 M40 55 L60 55" stroke="#6a4c93" strokeWidth="3"/>
                  <defs>
                    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" style={{stopColor: '#a83279'}} />
                      <stop offset="100%" style={{stopColor: '#6a4c93'}} />
                    </linearGradient>
                  </defs>
                </svg>
              </div>
            </div>
            
            <FormularioLiga
              onSubmit={handleFormSubmit}
              onCancel={handleFormCancel}
              initialData={editingLiga}
              isEditing={!!editingLiga}
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`ligas-container ${hasVisited ? 'no-animation' : ''}`}>
      <div className="ligas-background">
        <div className="ligas-wrapper">
          <div className="main-sticky-container">
            <TopBar user={user} onLogout={handleLogout} />
            
            <div className="sticky-controls">
              <LigasHeader onCreateClick={handleCreateClick} />
              <SearchBar searchTerm={searchTerm} onSearchChange={setSearchTerm} />
            </div>
          </div>

          <div className="ligas-content">
            {loading && (
              <div className="loading-container">
                <div className="loading-spinner"></div>
                <p>Cargando ligas...</p>
              </div>
            )}

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            {!loading && !error && (
              filteredLigas.length === 0 ? (
                <div className="empty-state">
                  <div className="empty-icon">
                    <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                      <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                      <polyline points="17 21 17 13 7 13 7 21"></polyline>
                      <polyline points="7 3 7 8 15 8"></polyline>
                    </svg>
                  </div>
                  <h3>No se encontraron ligas</h3>
                  <p>
                    {searchTerm 
                      ? 'No hay ligas que coincidan con tu búsqueda.' 
                      : 'Usa el botón "+ Nueva Liga" para comenzar.'
                    }
                  </p>
                </div>
              ) : (
                <div className="ligas-grid">
                  {filteredLigas.map((liga) => (
                    <TarjetaLiga
                      key={liga.id_liga}
                      liga={liga}
                      onEdit={handleEditClick}
                      onDelete={handleDeleteLiga}
                      onView={handleViewLiga}
                      onVerTabla={handleVerTabla}
                    />
                  ))}
                </div>
              )
            )}

            <LigasModal 
              liga={viewingLiga} 
              onClose={() => setViewingLiga(null)}
              getEstadoColor={getEstadoColor}
            />
          </div>
        </div>

        <NotificacionesContainer 
          notificaciones={notificaciones}
          onClose={cerrarNotificacion}
        />

        <AlertaConfirmacion
          mostrar={alertaConfirmacion.mostrar}
          titulo={alertaConfirmacion.paso === 1 ? 'Confirmar Eliminación' : 'Última Advertencia'}
          mensaje={
            alertaConfirmacion.paso === 1 
              ? '¿Estás seguro de que quieres eliminar esta liga?'
              : 'Esta acción es irreversible. ¿Realmente deseas continuar?'
          }
          textoConfirmar={alertaConfirmacion.paso === 1 ? 'Continuar' : 'Sí, Eliminar'}
          textoCancelar={alertaConfirmacion.paso === 1 ? 'Cancelar' : 'No, Cancelar'}
          onConfirmar={confirmarEliminacion}
          onCancelar={cancelarEliminacion}
        />
      </div>
    </div>
  );
};

export default LigasPage;
