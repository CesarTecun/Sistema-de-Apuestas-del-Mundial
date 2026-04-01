import React, { useState } from 'react';

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

  return (
    <form className="form-container" onSubmit={handleSubmit}>
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      {/* Primera fila: Nombres */}
      <div className="input-group">
        <div className="input-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
        <input 
          type="text" 
          name="primer_nombre"
          placeholder="Primer Nombre" 
          className="form-input"
          value={formData.primer_nombre}
          onChange={handleChange}
          required
        />
      </div>

      <div className="input-group">
        <div className="input-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
        <input 
          type="text" 
          name="segundo_nombre"
          placeholder="Segundo Nombre" 
          className="form-input"
          value={formData.segundo_nombre}
          onChange={handleChange}
        />
      </div>

      {/* Segunda fila: Apellidos */}
      <div className="input-group">
        <div className="input-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
        <input 
          type="text" 
          name="primer_apellido"
          placeholder="Primer Apellido" 
          className="form-input"
          value={formData.primer_apellido}
          onChange={handleChange}
          required
        />
      </div>

      <div className="input-group">
        <div className="input-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
        <input 
          type="text" 
          name="segundo_apellido"
          placeholder="Segundo Apellido" 
          className="form-input"
          value={formData.segundo_apellido}
          onChange={handleChange}
        />
      </div>

      {/* Tercera fila: Teléfono y Fecha */}
      <div className="input-group telefono-field">
        <div className="input-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
          </svg>
        </div>
        <input 
          type="tel" 
          name="telefono"
          placeholder="Teléfono" 
          className="form-input"
          value={formData.telefono}
          onChange={handleChange}
        />
      </div>

      <div className="input-group fecha-field">
        <div className="input-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
        </div>
        <input 
          type="date" 
          name="fecha_nacimiento"
          placeholder="Fecha de Nacimiento" 
          className="form-input"
          value={formData.fecha_nacimiento}
          onChange={handleChange}
        />
      </div>
      
      {/* Cuarta fila: Correo (ancho completo) */}
      <div className="input-group email-field">
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
      
      {/* Quinta fila: Contraseña (ancho completo) */}
      <div className="input-group email-field">
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
      
      {/* Sexta fila: Confirmar Contraseña (ancho completo) */}
      <div className="input-group email-field">
        <div className="input-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
        </div>
        <input 
          type="password" 
          name="password2"
          placeholder="Confirmar Contraseña" 
          className="form-input"
          value={formData.password2}
          onChange={handleChange}
          required
        />
      </div>
      
      <button 
        type="submit" 
        className="registro-button"
        disabled={loading}
      >
        {loading ? 'Registrando...' : 'REGISTRARSE'}
      </button>
      
      <div className="form-links">
        <div className="login-link">
          <span>¿Ya tienes una cuenta? </span>
          <a href="/login" className="login-anchor">Inicia sesión</a>
        </div>
      </div>
    </form>
  );
};

export default FormularioRegistro;
