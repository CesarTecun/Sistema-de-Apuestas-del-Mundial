import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const FormularioRegistro = ({ onSubmit, error, loading }) => {
  const [formData, setFormData] = useState({
    primer_nombre: '',
    segundo_nombre: '',
    primer_apellido: '',
    segundo_apellido: '',
    email: '',
    telefono: '',
    fecha_nacimiento: '',
    password: '',
    password2: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showPassword2, setShowPassword2] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validar que las contraseñas coincidan
    if (formData.password !== formData.password2) {
      onSubmit({ error: 'Las contraseñas no coinciden' });
      return;
    }
    
    // Eliminar password2 del formData antes de enviar
    const { password2, ...dataToSend } = formData;
    console.log('Datos que se enviarán desde el formulario:', dataToSend);
    onSubmit(dataToSend);
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const togglePassword2Visibility = () => {
    setShowPassword2(!showPassword2);
  };

  return (
    <form className="form-container" onSubmit={handleSubmit}>
      <div className="form-header">
        <h2 className="registro-title">Crear Cuenta</h2>
        <p className="registro-subtitle">Únete a la emoción del Mundial 2026</p>
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
        {/* Primera fila: Primer Nombre y Primer Apellido en 2 columnas */}
        <div className="form-row form-row-compact">
          <div className="input-group">
            <label className="input-label" htmlFor="primer_nombre">Primer Nombre</label>
            <div className="input-wrapper">
              <div className="input-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
              </div>
              <input 
                id="primer_nombre"
                type="text" 
                name="primer_nombre"
                placeholder="Juan" 
                className="form-input"
                value={formData.primer_nombre}
                onChange={handleChange}
                required
                autoComplete="given-name"
              />
            </div>
          </div>

          <div className="input-group">
            <label className="input-label" htmlFor="primer_apellido">Primer Apellido</label>
            <div className="input-wrapper">
              <div className="input-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
              </div>
              <input 
                id="primer_apellido"
                type="text" 
                name="primer_apellido"
                placeholder="Pérez" 
                className="form-input"
                value={formData.primer_apellido}
                onChange={handleChange}
                required
                autoComplete="family-name"
              />
            </div>
          </div>
        </div>

        {/* Segunda fila: Segundo Nombre y Segundo Apellido en 2 columnas */}
        <div className="form-row form-row-compact">
          <div className="input-group">
            <label className="input-label" htmlFor="segundo_nombre">Segundo Nombre</label>
            <div className="input-wrapper">
              <div className="input-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
              </div>
              <input 
                id="segundo_nombre"
                type="text" 
                name="segundo_nombre"
                placeholder="Carlos" 
                className="form-input"
                value={formData.segundo_nombre}
                onChange={handleChange}
                autoComplete="additional-name"
              />
            </div>
          </div>

          <div className="input-group">
            <label className="input-label" htmlFor="segundo_apellido">Segundo Apellido</label>
            <div className="input-wrapper">
              <div className="input-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
              </div>
              <input 
                id="segundo_apellido"
                type="text" 
                name="segundo_apellido"
                placeholder="López" 
                className="form-input"
                value={formData.segundo_apellido}
                onChange={handleChange}
                autoComplete="additional-name"
              />
            </div>
          </div>
        </div>

        {/* Teléfono y Fecha en 2 columnas */}
        <div className="form-row form-row-compact">
          <div className="input-group">
            <label className="input-label" htmlFor="telefono">Teléfono</label>
            <div className="input-wrapper">
              <div className="input-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                  <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
                </svg>
              </div>
              <input 
                id="telefono"
                type="tel" 
                name="telefono"
                placeholder="+502 1234-5678" 
                className="form-input"
                value={formData.telefono}
                onChange={handleChange}
                autoComplete="tel"
              />
            </div>
          </div>

          <div className="input-group">
            <label className="input-label" htmlFor="fecha_nacimiento">Fecha de Nacimiento</label>
            <div className="input-wrapper">
              <div className="input-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
              </div>
              <input 
                id="fecha_nacimiento"
                type="date" 
                name="fecha_nacimiento"
                className="form-input"
                value={formData.fecha_nacimiento}
                onChange={handleChange}
                autoComplete="bday"
              />
            </div>
          </div>
        </div>
        
        {/* Cuarta fila: Correo (ancho completo) */}
        <div className="input-group full-width">
          <label className="input-label" htmlFor="email">Correo Electrónico</label>
          <div className="input-wrapper">
            <div className="input-icon">
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
              autoComplete="email"
            />
          </div>
        </div>
        
        {/* Quinta fila: Contraseñas en 2 columnas */}
        <div className="form-row form-row-compact">
          <div className="input-group">
            <label className="input-label" htmlFor="password">Contraseña</label>
            <div className="input-wrapper">
              <div className="input-icon">
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
                autoComplete="new-password"
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

          <div className="input-group">
            <label className="input-label" htmlFor="password2">Confirmar Contraseña</label>
            <div className="input-wrapper">
              <div className="input-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </div>
              <input 
                id="password2"
                type={showPassword2 ? 'text' : 'password'}
                name="password2"
                placeholder="••••••••" 
                className="form-input"
                value={formData.password2}
                onChange={handleChange}
                required
                autoComplete="new-password"
              />
              <button
                type="button"
                className="password-toggle"
                onClick={togglePassword2Visibility}
                aria-label={showPassword2 ? 'Ocultar contraseña' : 'Mostrar contraseña'}
              >
                {showPassword2 ? (
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
      </div>
      
      <button 
        type="submit" 
        className="registro-button"
        disabled={loading}
      >
        {loading ? (
          <span className="button-content">
            <svg className="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"></path>
            </svg>
            Registrando...
          </span>
        ) : (
          'CREAR CUENTA'
        )}
      </button>
      
      <div className="form-footer">
        <div className="login-link">
          <span>¿Ya tienes una cuenta? </span>
          <Link to="/login" className="login-anchor">Inicia sesión</Link>
        </div>
      </div>
    </form>
  );
};

export default FormularioRegistro;
