import React, { useState } from 'react';

const FormularioLogin = ({ onSubmit, error, loading }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form className="form-container" onSubmit={handleSubmit}>
      <h2 className="login-title">Bienvenido</h2>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      <div className="input-group">
        <div className="input-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="2" y="4" width="20" height="16" rx="2"></rect>
            <path d="m22 7-10 5L2 7"></path>
          </svg>
        </div>
        <input 
          type="email" 
          name="email"
          placeholder="Correo Electrónico" 
          className="form-input"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>
      
      <div className="input-group">
        <div className="input-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
        </div>
        <input 
          type="password" 
          name="password"
          placeholder="Contraseña" 
          className="form-input"
          value={formData.password}
          onChange={handleChange}
          required
        />
      </div>
      
      <button 
        type="submit" 
        className="login-button"
        disabled={loading}
      >
        {loading ? 'Iniciando sesión...' : 'INICIAR SESIÓN'}
      </button>
      
      <div className="form-links">
        <div className="remember-forgot">
          <label className="remember-me">
            <input type="checkbox" />
            <span>Recordarme</span>
          </label>
          <a href="#" className="forgot-password">¿Olvidaste tu contraseña?</a>
        </div>
        
        <div className="register-link">
          <span>¿No tienes una cuenta? </span>
          <a href="/registro" className="register-anchor">Regístrate</a>
        </div>
      </div>
    </form>
  );
};

export default FormularioLogin;
