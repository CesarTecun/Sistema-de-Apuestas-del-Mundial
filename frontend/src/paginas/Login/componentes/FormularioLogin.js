import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const FormularioLogin = ({ onSubmit, error, loading }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false
  });
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleForgotPassword = () => {
    // TODO: Implementar modal o navegación para recuperación de contraseña
    console.log('Funcionalidad de recuperación de contraseña pendiente');
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <form className="form-container" onSubmit={handleSubmit}>
      <div className="form-header">
        <h2 className="login-title">Bienvenido</h2>
        <p className="login-subtitle">Inicia sesión en tu cuenta</p>
      </div>
      
      {error && (
        <div className="error-message">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <span>{error}</span>
        </div>
      )}
      
      <div className="form-fields">
        <div className="input-group">
          <label className="input-label" htmlFor="email">Correo Electrónico</label>
          <div className="input-wrapper">
            <div className="input-icon" aria-hidden="true">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="2" y="4" width="20" height="16" rx="2"></rect>
                <path d="m22 7-10 5L2 7"></path>
              </svg>
            </div>
            <input 
              id="email"
              type="email" 
              name="email"
              placeholder="tu@email.com" 
              className="form-input"
              value={formData.email}
              onChange={handleChange}
              required
              aria-label="Correo electrónico"
              autoComplete="email"
            />
          </div>
        </div>
        
        <div className="input-group">
          <label className="input-label" htmlFor="password">Contraseña</label>
          <div className="input-wrapper">
            <div className="input-icon" aria-hidden="true">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
            </div>
            <input 
              id="password"
              type={showPassword ? 'text' : 'password'}
              name="password"
              placeholder="••••••••" 
              className="form-input"
              value={formData.password}
              onChange={handleChange}
              required
              aria-label="Contraseña"
              autoComplete="current-password"
            />
            <button
              type="button"
              className="password-toggle"
              onClick={togglePasswordVisibility}
              aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
            >
              {showPassword ? (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                  <line x1="1" y1="1" x2="23" y2="23"></line>
                </svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>
      
      <div className="form-options">
        <label className="remember-me">
          <input 
            type="checkbox" 
            name="rememberMe"
            checked={formData.rememberMe}
            onChange={handleChange}
          />
          <span>Recordarme</span>
        </label>
        <button 
          type="button" 
          className="forgot-password"
          onClick={handleForgotPassword}
        >
          ¿Olvidaste tu contraseña?
        </button>
      </div>
      
      <button 
        type="submit" 
        className="login-button"
        disabled={loading}
        aria-disabled={loading}
      >
        {loading ? (
          <span className="button-content">
            <svg className="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"></path>
            </svg>
            Iniciando sesión...
          </span>
        ) : (
          'INICIAR SESIÓN'
        )}
      </button>
      
      <div className="form-footer">
        <div className="register-link">
          <span>¿No tienes una cuenta? </span>
          <Link to="/registro" className="register-anchor">Regístrate gratis</Link>
        </div>
      </div>
    </form>
  );
};

export default FormularioLogin;
