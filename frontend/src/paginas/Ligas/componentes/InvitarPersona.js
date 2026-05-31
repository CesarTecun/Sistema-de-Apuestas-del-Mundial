import React, { useState } from 'react';
import servicioLigas from '../../../servicios/servicioLigas';
import './InvitarPersona.css';

const InvitarPersona = ({ liga, onClose, onSuccess }) => {
  const [email, setEmail] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const result = await servicioLigas.enviarInvitacion(liga.id_liga, {
      email_invitado: email,
      mensaje_invitacion: mensaje,
    });

    if (result.success) {
      // onSuccess('Invitación enviada exitosamente');
      onClose();
    } else {
      // Mejorar mensaje de error para invitaciones duplicadas
      const errorMessage = result.error || 'Error al enviar invitación';
      if (errorMessage.includes('ya existe') || errorMessage.includes('duplicate') || errorMessage.includes('ya invitado')) {
        setError('Este usuario ya ha sido invitado a esta liga.');
      } else if (errorMessage.includes('ya es participante') || errorMessage.includes('ya miembro')) {
        setError('Este usuario ya es miembro de esta liga.');
      } else {
        setError(errorMessage);
      }
    }
    setLoading(false);
  };

  return (
    <div className="invitar-persona-overlay">
      <div className="invitar-persona-modal">
        <div className="invitar-persona-header">
          <h2>Invitar a {liga.nombre_liga}</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        <form onSubmit={handleSubmit} className="invitar-persona-form">
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="email">Correo electrónico del invitado:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="ejemplo@correo.com"
            />
          </div>

          <div className="form-group">
            <label htmlFor="mensaje">Mensaje (opcional):</label>
            <textarea
              id="mensaje"
              value={mensaje}
              onChange={(e) => setMensaje(e.target.value)}
              placeholder="Añade un mensaje personalizado..."
              rows={4}
            />
          </div>

          <div className="form-actions">
            <button
              type="button"
              className="btn-cancel"
              onClick={onClose}
              disabled={loading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="btn-submit"
              disabled={loading}
            >
              {loading ? 'Enviando...' : 'Enviar Invitación'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default InvitarPersona;
