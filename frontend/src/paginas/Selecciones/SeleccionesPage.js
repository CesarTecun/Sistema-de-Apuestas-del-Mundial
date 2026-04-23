import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import TarjetaSeleccion from './componentes/TarjetaSeleccion';
import FormularioSeleccion from './componentes/FormularioSeleccion';
import TopBar from './componentes/TopBar';
import SeleccionesHeader from './componentes/SeleccionesHeader';
import SearchBar from '../Ligas/componentes/SearchBar';
import useNotificaciones from '../../hooks/useNotificaciones';
import { useSelecciones } from '../../hooks/useSelecciones';
import NotificacionesContainer from '../../componentes/NotificacionesContainer';
import AlertaConfirmacion from '../Ligas/componentes/AlertaConfirmacion';
import '../../estilos/componentes/modals.css';
import './estilos/SeleccionesPage.css';

// Error Boundary para capturar errores de renderizado
class SeleccionesErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error en SeleccionesPage:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ 
          padding: '20px', 
          textAlign: 'center',
          color: 'white' 
        }}>
          <h2>Error al cargar Selecciones</h2>
          <p>{this.state.error?.message || 'Error desconocido'}</p>
          <button onClick={() => window.location.reload()}>Recargar página</button>
        </div>
      );
    }

    return this.props.children;
  }
}

const SeleccionesPage = () => {
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
    filteredSelecciones,
    createSeleccion,
    updateSeleccion,
    deleteSeleccion
  } = useSelecciones();

  const [showForm, setShowForm] = useState(false);
  const [editingSeleccion, setEditingSeleccion] = useState(null);
  const [alertaConfirmacion, setAlertaConfirmacion] = useState({
    mostrar: false,
    paso: 1,
    seleccionId: null
  });
  const [hasVisited, setHasVisited] = useState(false);

  useEffect(() => {
    const visited = sessionStorage.getItem('selecciones_visited');
    if (visited) {
      setHasVisited(true);
    } else {
      sessionStorage.setItem('selecciones_visited', 'true');
    }
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate('/home');
  };

  const handleFormSubmit = async (formData) => {
    const result = editingSeleccion
      ? await updateSeleccion(editingSeleccion.id_seleccion, formData)
      : await createSeleccion(formData);

    if (result.success) {
      setShowForm(false);
      setEditingSeleccion(null);
      success(editingSeleccion ? '¡Selección actualizada exitosamente!' : '¡Selección creada exitosamente!');
    } else {
      mostrarError(result.error || 'Error al procesar la operación');
    }
  };

  const handleFormCancel = () => {
    const scrollPosition = window.scrollY || document.documentElement.scrollTop;
    setShowForm(false);
    setEditingSeleccion(null);
    setTimeout(() => {
      window.scrollTo(0, scrollPosition);
    }, 50);
  };

  const handleEditClick = (seleccion) => {
    setEditingSeleccion(seleccion);
    setShowForm(true);
  };

  const handleCreateClick = () => {
    setEditingSeleccion(null);
    setShowForm(true);
  };

  const handleDeleteSeleccion = (seleccionId) => {
    setAlertaConfirmacion({
      mostrar: true,
      paso: 1,
      seleccionId: seleccionId
    });
  };

  const confirmarEliminacion = async () => {
    if (alertaConfirmacion.paso === 1) {
      setAlertaConfirmacion({
        ...alertaConfirmacion,
        paso: 2
      });
    } else {
      const result = await deleteSeleccion(alertaConfirmacion.seleccionId);
      if (result.success) {
        success('Selección eliminada exitosamente');
      } else {
        mostrarError(result.error || 'Error al eliminar selección');
      }
      setAlertaConfirmacion({ mostrar: false, paso: 1, seleccionId: null });
    }
  };

  const cancelarEliminacion = () => {
    setAlertaConfirmacion({ mostrar: false, paso: 1, seleccionId: null });
  };

  if (showForm) {
    return (
      <div className="selecciones-container">
        <div className="selecciones-background">
          <div className="selecciones-form-container">
            <div className="logo-container">
              <div className="logo">
                <svg width="100" height="100" viewBox="0 0 100 100" fill="none">
                  <circle cx="50" cy="50" r="45" fill="url(#gradient)" opacity="0.9"/>
                  <circle cx="50" cy="50" r="30" stroke="white" strokeWidth="3" fill="none"/>
                  <path d="M50 25 L50 75 M25 50 L75 50" stroke="white" strokeWidth="3"/>
                  <defs>
                    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" style={{stopColor: '#d4af37'}} />
                      <stop offset="100%" style={{stopColor: '#a83279'}} />
                    </linearGradient>
                  </defs>
                </svg>
              </div>
            </div>

            <FormularioSeleccion
              onSubmit={handleFormSubmit}
              onCancel={handleFormCancel}
              initialData={editingSeleccion}
              isEditing={!!editingSeleccion}
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`selecciones-container ${hasVisited ? 'no-animation' : ''}`}>
      <div className="selecciones-background">
        <div className="selecciones-wrapper">
          <div className="main-sticky-container">
            <TopBar user={user} onLogout={handleLogout} />

            <div className="sticky-controls">
              <SeleccionesHeader onCreateClick={handleCreateClick} />
              <SearchBar searchTerm={searchTerm} onSearchChange={setSearchTerm} />
            </div>
          </div>

          <div className="selecciones-content">
            {loading && (
              <div className="loading-container">
                <div className="loading-spinner"></div>
                <p>Cargando selecciones...</p>
              </div>
            )}

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            {!loading && !error && (
              filteredSelecciones.length === 0 ? (
                <div className="empty-state">
                  <div className="empty-icon">
                    <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="2" y1="12" x2="22" y2="12"></line>
                      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                    </svg>
                  </div>
                  <h3>No se encontraron selecciones</h3>
                  <p>
                    {searchTerm
                      ? 'No hay selecciones que coincidan con tu búsqueda.'
                      : 'Usa el botón "+ Nueva Selección" para comenzar.'
                    }
                  </p>
                </div>
              ) : (
                <div className="selecciones-grid">
                  {filteredSelecciones.map((seleccion) => (
                    <TarjetaSeleccion
                      key={seleccion.id_seleccion}
                      seleccion={seleccion}
                      onEdit={handleEditClick}
                      onDelete={handleDeleteSeleccion}
                    />
                  ))}
                </div>
              )
            )}
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
              ? '¿Estás seguro de que quieres eliminar esta selección?'
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

const SeleccionesPageWithBoundary = () => (
  <SeleccionesErrorBoundary>
    <SeleccionesPage />
  </SeleccionesErrorBoundary>
);

export default SeleccionesPageWithBoundary;
