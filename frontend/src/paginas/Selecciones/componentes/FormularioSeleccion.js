import React, { useState, useEffect } from 'react';
import '../estilos/FormularioSeleccion.css';

const FormularioSeleccion = ({ onSubmit, onCancel, initialData, isEditing }) => {
  const [formData, setFormData] = useState({
    pais: '',
    bandera: '',
    fk_id_fase_inicial: ''
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (initialData) {
      setFormData({
        pais: initialData.pais || '',
        bandera: initialData.bandera || '',
        fk_id_fase_inicial: initialData.fk_id_fase_inicial || ''
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Limpiar error del campo cuando el usuario empieza a escribir
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.pais) {
      newErrors.pais = 'El nombre del país es requerido';
    }
    
    if (!formData.bandera) {
      newErrors.bandera = 'La URL de la bandera es requerida';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      const dataToSubmit = {
        ...formData,
        fk_id_fase_inicial: formData.fk_id_fase_inicial ? parseInt(formData.fk_id_fase_inicial) : null
      };
      onSubmit(dataToSubmit);
    }
  };

  return (
    <div className="formulario-seleccion-container">
      <div className="form-header">
        <h2>{isEditing ? 'Editar Selección' : 'Nueva Selección'}</h2>
        <button className="close-btn" onClick={onCancel}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <form onSubmit={handleSubmit} className="seleccion-form">
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="pais">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                <path d="M2 12h20"></path>
              </svg>
              País *
            </label>
            <input
              type="text"
              id="pais"
              name="pais"
              value={formData.pais}
              onChange={handleChange}
              placeholder="Ej: México, Argentina, Brasil"
              className={errors.pais ? 'error' : ''}
            />
            {errors.pais && <span className="error-message">{errors.pais}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="bandera">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <image href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIj4KICA8cmVjdCB4PSIzIiB5PSIzIiB3aWR0aD0iMTgiIGhlaWdodD0iMTgiIHJ4PSIyIiByeT0iMiIvPgo8L3N2Zz4=" />
              </svg>
              URL de Bandera *
            </label>
            <input
              type="url"
              id="bandera"
              name="bandera"
              value={formData.bandera}
              onChange={handleChange}
              placeholder="https://ejemplo.com/bandera.png"
              className={errors.bandera ? 'error' : ''}
            />
            {errors.bandera && <span className="error-message">{errors.bandera}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="fk_id_fase_inicial">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                <polyline points="2 17 12 22 22 17"></polyline>
              </svg>
              Fase Inicial (ID)
            </label>
            <input
              type="number"
              id="fk_id_fase_inicial"
              name="fk_id_fase_inicial"
              value={formData.fk_id_fase_inicial}
              onChange={handleChange}
              placeholder="Opcional"
            />
          </div>
        </div>

        <div className="form-actions">
          <button type="button" className="cancel-btn" onClick={onCancel}>
            Cancelar
          </button>
          <button type="submit" className="submit-btn">
            {isEditing ? 'Actualizar Selección' : 'Crear Selección'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default FormularioSeleccion;
