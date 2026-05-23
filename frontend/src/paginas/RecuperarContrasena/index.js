import React, { useEffect, useMemo, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';

import { API_ENDPOINTS } from '../../config/apiConfig';
import LogoCopaMundial from '../Login/componentes/LogoCopaMundial';
import './estilos/RecuperarContrasena.css';

const initialFeedback = { status: 'idle', message: '' };

const RecuperarContrasenaPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const token = useMemo(() => new URLSearchParams(location.search).get('token'), [location.search]);
  const hasToken = Boolean(token);

  const [email, setEmail] = useState('');
  const [requestFeedback, setRequestFeedback] = useState(initialFeedback);
  const [requestLoading, setRequestLoading] = useState(false);

  const [passwordData, setPasswordData] = useState({ password: '', password2: '' });
  const [resetFeedback, setResetFeedback] = useState(initialFeedback);
  const [resetLoading, setResetLoading] = useState(false);
  const [showPasswords, setShowPasswords] = useState(false);

  useEffect(() => {
    if (resetFeedback.status === 'success') {
      const timeout = setTimeout(() => navigate('/login'), 2500);
      return () => clearTimeout(timeout);
    }
  }, [resetFeedback, navigate]);

  const handleRequestSubmit = async (event) => {
    event.preventDefault();
    setRequestLoading(true);
    setRequestFeedback(initialFeedback);

    try {
      await axios.post(API_ENDPOINTS.AUTH.PASSWORD_RESET_REQUEST, { email });
      setRequestFeedback({
        status: 'success',
        message: 'Si el correo existe, recibirás un enlace para restablecer la contraseña en los próximos minutos.'
      });
    } catch (error) {
      const message =
        error.response?.data?.message ||
        error.response?.data?.error ||
        'No fue posible enviar el correo en este momento. Intenta nuevamente.';
      setRequestFeedback({ status: 'error', message });
    } finally {
      setRequestLoading(false);
    }
  };

  const handleResetSubmit = async (event) => {
    event.preventDefault();
    setResetLoading(true);
    setResetFeedback(initialFeedback);

    try {
      await axios.post(API_ENDPOINTS.AUTH.PASSWORD_RESET_CONFIRM, {
        token,
        password: passwordData.password,
        password2: passwordData.password2,
      });
      setResetFeedback({
        status: 'success',
        message: 'Contraseña actualizada. Redireccionando al inicio de sesión...',
      });
      setPasswordData({ password: '', password2: '' });
    } catch (error) {
      const message =
        error.response?.data?.password?.[0] ||
        error.response?.data?.token ||
        error.response?.data?.message ||
        'No pudimos actualizar la contraseña. Verifica el token o intenta de nuevo.';
      setResetFeedback({ status: 'error', message });
    } finally {
      setResetLoading(false);
    }
  };

  const toggleShowPasswords = () => setShowPasswords((prev) => !prev);

  return (
    <div className="recovery-page">
      <div className="recovery-panel">
        <div className="recovery-logo">
          <LogoCopaMundial size={120} />
        </div>
        <div className="recovery-content">
          <h1>{hasToken ? 'Restablece tu contraseña' : 'Recupera tu acceso'}</h1>
          <p>
            {hasToken
              ? 'Crea una nueva contraseña segura para continuar disfrutando del sistema.'
              : 'Ingresa tu correo electrónico y te enviaremos instrucciones para recuperar tu acceso.'}
          </p>

          {!hasToken && (
            <form className="recovery-form" onSubmit={handleRequestSubmit}>
              <label htmlFor="email">Correo electrónico</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="tucorreo@ejemplo.com"
                required
              />

              {requestFeedback.status !== 'idle' && (
                <div className={`recovery-alert recovery-alert--${requestFeedback.status}`}>
                  {requestFeedback.message}
                </div>
              )}

              <button type="submit" className="recovery-button" disabled={requestLoading}>
                {requestLoading ? 'Enviando enlace...' : 'Enviar instrucciones'}
              </button>

              <p className="recovery-hint">
                ¿No encuentras el correo? Revisa spam o <span>promociones</span>.
              </p>
            </form>
          )}

          {hasToken && (
            <form className="recovery-form" onSubmit={handleResetSubmit}>
              <label htmlFor="password">Nueva contraseña</label>
              <div className="password-field">
                <input
                  id="password"
                  type={showPasswords ? 'text' : 'password'}
                  value={passwordData.password}
                  onChange={(event) =>
                    setPasswordData((prev) => ({ ...prev, password: event.target.value }))
                  }
                  placeholder="••••••••"
                  required
                />
                <button type="button" className="toggle-visibility" onClick={toggleShowPasswords}>
                  {showPasswords ? 'Ocultar' : 'Mostrar'}
                </button>
              </div>

              <label htmlFor="password2">Confirma tu contraseña</label>
              <input
                id="password2"
                type={showPasswords ? 'text' : 'password'}
                value={passwordData.password2}
                onChange={(event) =>
                  setPasswordData((prev) => ({ ...prev, password2: event.target.value }))
                }
                placeholder="••••••••"
                required
              />

              <ul className="password-hints">
                <li>Debe tener al menos 8 caracteres.</li>
                <li>Combina letras mayúsculas, minúsculas, números y símbolos.</li>
              </ul>

              {resetFeedback.status !== 'idle' && (
                <div className={`recovery-alert recovery-alert--${resetFeedback.status}`}>
                  {resetFeedback.message}
                </div>
              )}

              <button type="submit" className="recovery-button" disabled={resetLoading}>
                {resetLoading ? 'Actualizando...' : 'Guardar nueva contraseña'}
              </button>
            </form>
          )}

          <div className="recovery-footer">
            <Link to="/login">Volver al inicio de sesión</Link>
            {!hasToken && (
              <button
                type="button"
                className="recovery-contact"
                onClick={() => navigate('/registro')}
              >
                ¿No tienes cuenta? Regístrate
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecuperarContrasenaPage;
