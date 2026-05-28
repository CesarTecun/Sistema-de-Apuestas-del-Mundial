import React, { useState } from 'react';
import axios from 'axios';
import { API_ENDPOINTS, getAuthHeaders } from '../../../config/apiConfig';
import './BuzonInvitaciones.css';

const BuzonInvitaciones = ({ invitaciones, loading, onInvitacionAceptada }) => {
  const [procesando, setProcesando] = useState({});
  const [error, setError] = useState(null);

  const handleAceptarInvitacion = async (invitacion) => {
    setProcesando(prev => ({ ...prev, [invitacion.id_invitacion]: true }));
    setError(null);

    try {
      const response = await axios.post(
        API_ENDPOINTS.INVITACION_PUBLICA(invitacion.codigo_invitacion),
        { email: invitacion.email_invitado },
        { headers: getAuthHeaders() }
      );

      if (response.data.access) {
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
      }

      onInvitacionAceptada();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al aceptar la invitación');
    } finally {
      setProcesando(prev => ({ ...prev, [invitacion.id_invitacion]: false }));
    }
  };

  const handleRechazarInvitacion = async (invitacion) => {
    setProcesando(prev => ({ ...prev, [invitacion.id_invitacion]: true }));
    setError(null);

    try {
      await axios.post(
        `${API_ENDPOINTS.INVITACIONES}${invitacion.id_invitacion}/rechazar/`,
        {},
        { headers: getAuthHeaders() }
      );

      onInvitacionAceptada();
    } catch (err) {
      setError(err.response?.data?.error || 'Error al rechazar la invitación');
    } finally {
      setProcesando(prev => ({ ...prev, [invitacion.id_invitacion]: false }));
    }
  };

  const invitacionesPendientes = invitaciones.filter(
    inv => inv.estado_invitacion === 'Pendiente'
  );

  if (loading) {
    return (
      <div className="buzon-container">
        <div className="buzon-header">
          <h2>Buzón de Invitaciones</h2>
        </div>
        <div className="buzon-loading">
          <div className="loading-spinner"></div>
          <p>Cargando invitaciones...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="buzon-container">
      <div className="buzon-header">
        <h2>Buzón de Invitaciones</h2>
        <span className="invitaciones-count">
          {invitacionesPendientes.length} pendiente{invitacionesPendientes.length !== 1 ? 's' : ''}
        </span>
      </div>

      {error && (
        <div className="buzon-error">
          {error}
        </div>
      )}

      {invitacionesPendientes.length === 0 ? (
        <div className="buzon-vacio">
          <div className="buzon-icon">📬</div>
          <h3>No tienes invitaciones pendientes</h3>
          <p>Cuando recibas una invitación a una liga, aparecerá aquí.</p>
        </div>
      ) : (
        <div className="invitaciones-lista">
          {invitacionesPendientes.map((invitacion) => (
            <div key={invitacion.id_invitacion} className="invitacion-card">
              <div className="invitacion-info">
                <div className="invitacion-liga">
                  <span className="invitacion-label">Liga:</span>
                  <span className="invitacion-valor">{invitacion.liga?.nombre_liga || 'Cargando...'}</span>
                </div>
                <div className="invitacion-mensaje">
                  {invitacion.mensaje_invitacion && (
                    <>
                      <span className="invitacion-label">Mensaje:</span>
                      <span className="invitacion-valor">{invitacion.mensaje_invitacion}</span>
                    </>
                  )}
                </div>
                <div className="invitacion-fecha">
                  <span className="invitacion-label">Enviada:</span>
                  <span className="invitacion-valor">
                    {new Date(invitacion.fecha_invitacion).toLocaleDateString()}
                  </span>
                </div>
              </div>
              <div className="invitacion-acciones">
                <button
                  className="btn-aceptar"
                  onClick={() => handleAceptarInvitacion(invitacion)}
                  disabled={procesando[invitacion.id_invitacion]}
                >
                  {procesando[invitacion.id_invitacion] ? 'Procesando...' : 'Aceptar'}
                </button>
                <button
                  className="btn-rechazar"
                  onClick={() => handleRechazarInvitacion(invitacion)}
                  disabled={procesando[invitacion.id_invitacion]}
                >
                  Rechazar
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BuzonInvitaciones;
