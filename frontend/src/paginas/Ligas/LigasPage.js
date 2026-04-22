import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import TarjetaLiga from './componentes/TarjetaLiga';
import FormularioLiga from './componentes/FormularioLiga';
import useNotificaciones from '../../hooks/useNotificaciones';
import NotificacionesContainer from '../../componentes/NotificacionesContainer';
import AlertaConfirmacion from './componentes/AlertaConfirmacion';
import { API_ENDPOINTS, getAuthHeaders } from '../../config/apiConfig';
import './componentes/AlertaConfirmacion.css';
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
  const [ligas, setLigas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingLiga, setEditingLiga] = useState(null);
  const [viewingLiga, setViewingLiga] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [alertaConfirmacion, setAlertaConfirmacion] = useState({
    mostrar: false,
    paso: 1,
    ligaId: null
  });

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const cargarLigas = async () => {
    try {
      setLoading(true);
      const response = await fetch(API_ENDPOINTS.LIGAS, {
        headers: getAuthHeaders()
      });
      
      if (!response.ok) {
        if (response.status === 401) {
          mostrarError('Sesión expirada. Por favor inicia sesión nuevamente.');
          logout();
          navigate('/login');
          return;
        }
        if (response.status === 404) {
          throw new Error('Endpoint no encontrado. El servidor puede no estar corriendo.');
        }
        throw new Error(`Error HTTP: ${response.status}`);
      }
      
      const data = await response.json();
      setLigas(data);
      setError('');
    } catch (error) {
      console.error('Error al cargar ligas:', error);
      setError('Error al cargar las ligas. Verifica que el backend esté corriendo.');
      mostrarError('No se pudieron cargar las ligas. Revisa tu conexión.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarLigas();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const handleCreateLiga = async (ligaData) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/ligas/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(ligaData),
      });

      if (response.ok) {
        const nuevaLiga = await response.json();
        setLigas([...ligas, nuevaLiga]);
        setShowForm(false);
        success('¡Liga creada exitosamente!');
      } else {
        if (response.status === 401) {
          mostrarError('Sesión expirada. Por favor inicia sesión nuevamente.');
          logout();
          navigate('/login');
          return;
        }
        const errorData = await response.json();
        mostrarError(`Error al crear liga: ${errorData.message || 'Intenta nuevamente'}`);
      }
    } catch (err) {
      console.error('Error al crear liga:', err);
      mostrarError('Error de conexión. Verifica tu internet e intenta nuevamente.');
    }
  };

  const handleEditLiga = async (ligaData) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://localhost:8000/api/ligas/${editingLiga.id_liga}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(ligaData),
      });

      if (response.ok) {
        const ligaActualizada = await response.json();
        setLigas(ligas.map(liga => 
          liga.id_liga === ligaActualizada.id_liga ? ligaActualizada : liga
        ));
        setShowForm(false);
        setEditingLiga(null);
        success('¡Liga actualizada exitosamente!');
      } else {
        if (response.status === 401) {
          mostrarError('Sesión expirada. Por favor inicia sesión nuevamente.');
          logout();
          navigate('/login');
          return;
        }
        const errorData = await response.json();
        mostrarError(`Error al actualizar liga: ${errorData.message || 'Intenta nuevamente'}`);
      }
    } catch (err) {
      console.error('Error al actualizar liga:', err);
      mostrarError('Error de conexión. Verifica tu internet e intenta nuevamente.');
    }
  };

  const handleEditClick = (liga) => {
    console.log('Editando liga:', liga); // Debug
    setEditingLiga(liga);
    setShowForm(true);
  };

  const handleCreateClick = () => {
    console.log('Creando nueva liga'); // Debug
    setEditingLiga(null);
    setShowForm(true);
  };

  const handleDeleteLiga = async (ligaId) => {
    // Mostrar primera confirmación
    setAlertaConfirmacion({
      mostrar: true,
      paso: 1,
      ligaId: ligaId
    });
  };

  const confirmarEliminacion = async () => {
    if (alertaConfirmacion.paso === 1) {
      // Segunda confirmación
      setAlertaConfirmacion({
        ...alertaConfirmacion,
        paso: 2
      });
    } else {
      // Ejecutar eliminación
      try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`http://localhost:8000/api/ligas/${alertaConfirmacion.ligaId}/`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          setLigas(ligas.filter(liga => liga.id_liga !== alertaConfirmacion.ligaId));
          success('Liga eliminada exitosamente');
        } else {
          if (response.status === 401) {
            mostrarError('Sesión expirada. Por favor inicia sesión nuevamente.');
            logout();
            navigate('/login');
            return;
          }
          const errorData = await response.json();
          mostrarError(`Error al eliminar liga: ${errorData.message || 'Intenta nuevamente'}`);
        }
      } catch (err) {
        console.error('Error al eliminar liga:', err);
        mostrarError('Error de conexión. Verifica tu internet e intenta nuevamente.');
      } finally {
        setAlertaConfirmacion({ mostrar: false, paso: 1, ligaId: null });
      }
    }
  };

  const cancelarEliminacion = () => {
    setAlertaConfirmacion({ mostrar: false, paso: 1, ligaId: null });
  };

  const handleFormSubmit = async (formData) => {
    if (editingLiga) {
      await handleEditLiga(formData);
    } else {
      await handleCreateLiga(formData);
    }
  };

  const handleFormCancel = () => {
    // Guardar la posición actual del scroll antes de cerrar el formulario
    const scrollPosition = window.scrollY || document.documentElement.scrollTop;
    
    // Cerrar el formulario
    setShowForm(false);
    setEditingLiga(null);
    
    // Restaurar la posición del scroll después de un pequeño retraso
    setTimeout(() => {
      window.scrollTo(0, scrollPosition);
    }, 50);
  };

  const handleViewLiga = (liga) => {
    setViewingLiga(liga);
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

  const filteredLigas = ligas.filter(liga =>
    liga.nombre_liga.toLowerCase().includes(searchTerm.toLowerCase()) ||
    liga.tipo_liga?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    liga.estado?.toLowerCase().includes(searchTerm.toLowerCase())
  );

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
    <div className="ligas-container">
      <div className="ligas-background">
        {/* Contenedor Principal Sticky - Usuario + Controles */}
        <div className="main-sticky-container">
          {/* Barra Superior - Admin Quiniela */}
          <div className="top-bar">
            <div className="user-info">
              <div className="user-avatar">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
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
                onClick={handleLogout}
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16 17 21 12 16 7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
                Cerrar Sesión
              </button>
            </div>
          </div>

          {/* Controles Adicionales */}
          <div className="sticky-controls">
            {/* Header con Título */}
            <div className="ligas-header">
              <div className="header-content">
                <h1 className="page-title">Ligas del Mundial</h1>
                <p className="page-subtitle">Gestiona las ligas de apuestas</p>
              </div>
              
              <button 
                className="create-button"
                onClick={handleCreateClick}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                Nueva Liga
              </button>
            </div>

            {/* Barra de Búsqueda */}
            <div className="search-container">
              <div className="search-input-group">
                <div className="search-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.35-4.35"></path>
                  </svg>
                </div>
                <input
                  type="text"
                  placeholder="Buscar ligas..."
                  className="search-input"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Contenido Principal - Ligas del Mundial */}
        <div className="ligas-content">

          {/* Loading */}
          {loading && (
            <div className="loading-container">
              <div className="loading-spinner"></div>
              <p>Cargando ligas...</p>
            </div>
          )}

          {/* Error */}
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          {/* Grid de Ligas - Aquí se mostrarán las ligas creadas */}
          {!loading && !error && (
            <div className="ligas-grid">
              {filteredLigas.length === 0 ? (
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
                // Aquí se renderizan las ligas creadas y almacenadas
                filteredLigas.map((liga) => (
                  <TarjetaLiga
                    key={liga.id_liga}
                    liga={liga}
                    onEdit={handleEditClick}
                    onDelete={handleDeleteLiga}
                    onView={handleViewLiga}
                  />
                ))
              )}
            </div>
          )}

          {/* Modal para ver detalles */}
          {viewingLiga && (
            <div className="modal-overlay" onClick={() => setViewingLiga(null)}>
              <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <button 
                  className="modal-close"
                  onClick={() => setViewingLiga(null)}
                >
                  ×
                </button>
                
                <div className="modal-header">
                  <h2>{viewingLiga.nombre_liga}</h2>
                  <div className="modal-badges">
                    <span className="badge tipo-badge">
                      {viewingLiga.tipo_liga || 'Diversion'}
                    </span>
                    <span 
                      className="badge estado-badge"
                      style={{ backgroundColor: getEstadoColor(viewingLiga.estado) }}
                    >
                      {viewingLiga.estado || 'Activa'}
                    </span>
                  </div>
                </div>
                
                <div className="modal-body">
                  <div className="detail-item">
                    <label>ID Liga:</label>
                    <span>{viewingLiga.id_liga}</span>
                  </div>
                  <div className="detail-item">
                    <label>Administrador:</label>
                    <span>{viewingLiga.fk_administrador || 'Sin asignar'}</span>
                  </div>
                  <div className="detail-item">
                    <label>Monto Recaudado:</label>
                    <span>
                      {new Intl.NumberFormat('es-GT', {
                        style: 'currency',
                        currency: 'GTQ'
                      }).format(viewingLiga.monto_total_recaudado)}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Contenedor de Notificaciones */}
      <NotificacionesContainer 
        notificaciones={notificaciones}
        onClose={cerrarNotificacion}
      />

      {/* Alerta de Confirmación Personalizada */}
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
  );
};

export default LigasPage;
