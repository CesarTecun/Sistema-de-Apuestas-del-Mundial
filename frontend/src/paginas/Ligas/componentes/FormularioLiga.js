import React, { useState, useEffect } from 'react';
import { useAuth } from '../../../contextos/ContextoAutenticacion';
import '../estilos/FormularioLiga.css';

const FormularioLiga = ({ onSubmit, onCancel, initialData, isEditing }) => {
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    nombre_liga: '',
    fk_administrador: user?.id_usuario || '', // Asignar automáticamente el ID del usuario logueado
    monto_total_recaudado: '0',
    estado: 'Activa',
    tipo_liga: 'Diversion'
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (initialData) {
      setFormData({
        nombre_liga: initialData.nombre_liga || '',
        fk_administrador: initialData.fk_administrador || user?.id_usuario || '',
        monto_total_recaudado: initialData.monto_total_recaudado?.toString() || '0',
        estado: initialData.estado || 'Activa',
        tipo_liga: initialData.tipo_liga || 'Diversion'
      });
    } else {
      // Para nuevas ligas, siempre asignar el ID del usuario logueado
      setFormData(prev => ({
        ...prev,
        fk_administrador: user?.id_usuario || ''
      }));
    }
  }, [initialData, user]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
    
    // Limpiar error del campo cuando se modifica
    if (errors[name]) {
      setErrors(prevErrors => ({
        ...prevErrors,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.nombre_liga.trim()) {
      newErrors.nombre_liga = 'El nombre de la liga es requerido';
    }
    
    if (!formData.tipo_liga) {
      newErrors.tipo_liga = 'El tipo de liga es requerido';
    }
    
    if (!formData.estado) {
      newErrors.estado = 'El estado es requerido';
    }
    
    if (formData.monto_total_recaudado && isNaN(formData.monto_total_recaudado)) {
      newErrors.monto_total_recaudado = 'El monto debe ser un número válido';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    // Crear objeto limpio solo con los campos necesarios
    const dataToSubmit = {
      nombre_liga: formData.nombre_liga?.trim() || '',
      fk_administrador: user?.id_usuario || parseInt(formData.fk_administrador) || null,
      monto_total_recaudado: parseFloat(formData.monto_total_recaudado) || 0,
      estado: formData.estado || 'Activa',
      tipo_liga: formData.tipo_liga || 'Diversion'
    };
    
    // Validar que no haya objetos React
    Object.keys(dataToSubmit).forEach(key => {
      const value = dataToSubmit[key];
      if (typeof value === 'object' && value !== null) {
        console.error(`Campo ${key} contiene objeto:`, value);
        delete dataToSubmit[key];
      }
    });
    
    console.log('Datos limpios a enviar:', dataToSubmit);
    onSubmit(dataToSubmit);
  };

  const tiposLiga = [
    { value: 'Diversion', label: 'Diversión' },
    { value: 'Competitiva', label: 'Competitiva' },
    { value: 'Dinero', label: 'Dinero' }
  ];

  const estados = [
    { value: 'Activa', label: 'Activa', color: '#4CAF50' },
    { value: 'Inactiva', label: 'Inactiva', color: '#f44336' },
    { value: 'Pendiente', label: 'Pendiente', color: '#FF9800' }
  ];

  return (
    <form className="liga-form-container" onSubmit={handleSubmit}>
      <h2 className="form-title">
        {isEditing ? 'Editar Liga' : 'Crear Nueva Liga'}
      </h2>
      
      {/* Campo Nombre de Liga */}
      <div className="form-group">
        <div className="input-group">
          <div className="input-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
            </svg>
          </div>
          <input
            type="text"
            name="nombre_liga"
            placeholder="Nombre de la Liga"
            className={`form-input ${errors.nombre_liga ? 'error' : ''}`}
            value={formData.nombre_liga}
            onChange={handleChange}
            required
          />
        </div>
        {errors.nombre_liga && (
          <div className="field-error">{errors.nombre_liga}</div>
        )}
      </div>

      {/* Campo Tipo de Liga */}
      <div className="form-group">
        <div className="input-group">
          <div className="input-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 6v6l4 2"/>
            </svg>
          </div>
          <select
            name="tipo_liga"
            className={`form-input ${errors.tipo_liga ? 'error' : ''}`}
            value={formData.tipo_liga}
            onChange={handleChange}
            required
          >
            <option value="">Seleccionar tipo de liga</option>
            {tiposLiga.map(tipo => (
              <option key={tipo.value} value={tipo.value}>
                {tipo.label}
              </option>
            ))}
          </select>
        </div>
        {errors.tipo_liga && (
          <div className="field-error">{errors.tipo_liga}</div>
        )}
      </div>

      {/* Campo Estado */}
      <div className="form-group">
        <div className="input-group">
          <div className="input-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
          </div>
          <select
            name="estado"
            className={`form-input ${errors.estado ? 'error' : ''}`}
            value={formData.estado}
            onChange={handleChange}
            required
          >
            <option value="">Seleccionar estado</option>
            {estados.map(estado => (
              <option key={estado.value} value={estado.value}>
                {estado.label}
              </option>
            ))}
          </select>
        </div>
        {errors.estado && (
          <div className="field-error">{errors.estado}</div>
        )}
      </div>

      {/* Campo ID Administrador - Oculto y automático */}
      <input
        type="hidden"
        name="fk_administrador"
        value={formData.fk_administrador}
        onChange={handleChange}
      />

      {/* Campo Monto Total Recaudado */}
      <div className="form-group">
        <div className="input-group">
          <div className="input-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="12" y1="1" x2="12" y2="23"/>
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
            </svg>
          </div>
          <input
            type="number"
            name="monto_total_recaudado"
            placeholder="Monto Total Recaudado"
            step="0.01"
            min="0"
            className={`form-input ${errors.monto_total_recaudado ? 'error' : ''}`}
            value={formData.monto_total_recaudado}
            onChange={handleChange}
          />
        </div>
        {errors.monto_total_recaudado && (
          <div className="field-error">{errors.monto_total_recaudado}</div>
        )}
      </div>

      {/* Botones de Acción */}
      <div className="form-actions">
        <button
          type="button"
          className="cancel-button"
          onClick={onCancel}
        >
          Cancelar
        </button>
        
        <button
          type="submit"
          className="submit-button"
        >
          {isEditing ? 'Actualizar Liga' : 'Crear Liga'}
        </button>
      </div>
    </form>
  );
};

export default FormularioLiga;
