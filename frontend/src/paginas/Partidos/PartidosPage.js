import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import TarjetaPartido from './componentes/TarjetaPartido';
import FormularioPartido from './componentes/FormularioPartido';
import TopBar from './componentes/TopBar';
import PartidosHeader from './componentes/PartidosHeader';
import SearchBar from '../Ligas/componentes/SearchBar';
import useNotificaciones from '../../hooks/useNotificaciones';
import { usePartidos } from '../../hooks/usePartidos';
import NotificacionesContainer from '../../componentes/NotificacionesContainer';
import AlertaConfirmacion from '../Ligas/componentes/AlertaConfirmacion';
import '../../estilos/componentes/modals.css';
import './estilos/PartidosPage.css';

// Error Boundary para capturar errores de renderizado
class PartidosErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error en PartidosPage:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ 
          padding: '20px', 
          textAlign: 'center',
          color: 'white' 
        }}>
          <h2>Error al cargar Partidos</h2>
          <p>{this.state.error?.message || 'Error desconocido'}</p>
          <button onClick={() => window.location.reload()}>Recargar página</button>
        </div>
      );
    }

    return this.props.children;
  }
}

const PartidosPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const {
    notificaciones,
    cerrarNotificacion,
    success,
    error: mostrarError
  } = useNotificaciones();

  const {
    selecciones,
    loading,
    error,
    searchTerm,
    setSearchTerm,
    filteredPartidos,
    createPartido,
    updatePartido,
    deletePartido
  } = usePartidos();

  const [showForm, setShowForm] = useState(false);
  const [editingPartido, setEditingPartido] = useState(null);
  const [alertaConfirmacion, setAlertaConfirmacion] = useState({
    mostrar: false,
    paso: 1,
    partidoId: null
  });
  const [hasVisited, setHasVisited] = useState(false);

  useEffect(() => {
    const visited = sessionStorage.getItem('partidos_visited');
    if (visited) {
      setHasVisited(true);
    } else {
      sessionStorage.setItem('partidos_visited', 'true');
    }
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate('/home');
  };

  const handleFormSubmit = async (formData) => {
    const result = editingPartido
      ? await updatePartido(editingPartido.id_partido, formData)
      : await createPartido(formData);

    if (result.success) {
      setShowForm(false);
      setEditingPartido(null);
      success(editingPartido ? '¡Partido actualizado exitosamente!' : '¡Partido creado exitosamente!');
    } else {
      mostrarError(result.error || 'Error al procesar la operación');
    }
  };

  const handleFormCancel = () => {
    const scrollPosition = window.scrollY || document.documentElement.scrollTop;
    setShowForm(false);
    setEditingPartido(null);
    setTimeout(() => {
      window.scrollTo(0, scrollPosition);
    }, 50);
  };

  const handleEditClick = (partido) => {
    setEditingPartido(partido);
    setShowForm(true);
  };

  const handleCreateClick = () => {
    setEditingPartido(null);
    setShowForm(true);
  };

  const handleDeletePartido = (partidoId) => {
    setAlertaConfirmacion({
      mostrar: true,
      paso: 1,
      partidoId: partidoId
    });
  };

  const confirmarEliminacion = async () => {
    if (alertaConfirmacion.paso === 1) {
      setAlertaConfirmacion({
        ...alertaConfirmacion,
        paso: 2
      });
    } else {
      const result = await deletePartido(alertaConfirmacion.partidoId);
      if (result.success) {
        success('Partido eliminado exitosamente');
      } else {
        mostrarError(result.error || 'Error al eliminar partido');
      }
      setAlertaConfirmacion({ mostrar: false, paso: 1, partidoId: null });
    }
  };

  const cancelarEliminacion = () => {
    setAlertaConfirmacion({ mostrar: false, paso: 1, partidoId: null });
  };

  if (showForm) {
    return (
      <div className="partidos-container">
        <div className="partidos-background">
          <div className="partidos-form-container">
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

            <FormularioPartido
              onSubmit={handleFormSubmit}
              onCancel={handleFormCancel}
              initialData={editingPartido}
              isEditing={!!editingPartido}
              selecciones={selecciones}
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`partidos-container ${hasVisited ? 'no-animation' : ''}`}>
      <div className="partidos-background">
        <div className="partidos-wrapper">
          <div className="main-sticky-container">
            <TopBar user={user} onLogout={handleLogout} />

            <div className="sticky-controls">
              <PartidosHeader onCreateClick={handleCreateClick} />
              <SearchBar searchTerm={searchTerm} onSearchChange={setSearchTerm} />
            </div>
          </div>

          <div className="partidos-content">
            {loading && (
              <div className="loading-container">
                <div className="loading-spinner"></div>
                <p>Cargando partidos...</p>
              </div>
            )}

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            {!loading && !error && (
              filteredPartidos.length === 0 ? (
                <div className="empty-state">
                  <div className="empty-icon">
                    <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="2" y1="12" x2="22" y2="12"></line>
                      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                    </svg>
                  </div>
                  <h3>No se encontraron partidos</h3>
                  <p>
                    {searchTerm
                      ? 'No hay partidos que coincidan con tu búsqueda.'
                      : 'Usa el botón "+ Nuevo Partido" para comenzar.'
                    }
                  </p>
                </div>
              ) : (
                <div className="partidos-grid">
                  {filteredPartidos.map((partido) => (
                    <TarjetaPartido
                      key={partido.id_partido}
                      partido={partido}
                      selecciones={selecciones}
                      onEdit={handleEditClick}
                      onDelete={handleDeletePartido}
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
              ? '¿Estás seguro de que quieres eliminar este partido?'
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

const PartidosPageWithBoundary = () => (
  <PartidosErrorBoundary>
    <PartidosPage />
  </PartidosErrorBoundary>
);

export default PartidosPageWithBoundary;
