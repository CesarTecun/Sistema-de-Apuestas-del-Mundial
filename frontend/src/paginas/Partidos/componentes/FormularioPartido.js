import React, { useState, useEffect } from 'react';
import '../estilos/FormularioPartido.css';

const FormularioPartido = ({ onSubmit, onCancel, initialData, isEditing, selecciones }) => {
  const [formData, setFormData] = useState({
    horario: '',
    equipo_local: '',
    equipo_visitante: '',
    fk_sede: '',
    fk_id_fase: '',
    tipo_partido: 'Regular',
    gol_local: 0,
    gol_visitante: 0,
    resultado: ''
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (initialData) {
      setFormData({
        horario: initialData.horario || '',
        equipo_local: initialData.equipo_local || '',
        equipo_visitante: initialData.equipo_visitante || '',
        fk_sede: initialData.fk_sede || '',
        fk_id_fase: initialData.fk_id_fase || '',
        tipo_partido: initialData.tipo_partido || 'Regular',
        gol_local: initialData.gol_local || 0,
        gol_visitante: initialData.gol_visitante || 0,
        resultado: initialData.resultado || ''
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
    
    if (!formData.horario) {
      newErrors.horario = 'La fecha y hora son requeridas';
    }
    
    if (!formData.equipo_local) {
      newErrors.equipo_local = 'El equipo local es requerido';
    }
    
    if (!formData.equipo_visitante) {
      newErrors.equipo_visitante = 'El equipo visitante es requerido';
    }
    
    if (formData.equipo_local === formData.equipo_visitante) {
      newErrors.equipo_visitante = 'El equipo visitante debe ser diferente al local';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      const dataToSubmit = {
        ...formData,
        horario: new Date(formData.horario).toISOString(),
        gol_local: parseInt(formData.gol_local) || 0,
        gol_visitante: parseInt(formData.gol_visitante) || 0,
        fk_sede: formData.fk_sede ? parseInt(formData.fk_sede) : null,
        fk_id_fase: formData.fk_id_fase ? parseInt(formData.fk_id_fase) : null
      };
      onSubmit(dataToSubmit);
    }
  };

  return (
    <div className="formulario-partido-container">
      <div className="form-header">
        <h2>{isEditing ? 'Editar Partido' : 'Nuevo Partido'}</h2>
        <button className="close-btn" onClick={onCancel}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <form onSubmit={handleSubmit} className="partido-form">
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="horario">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
              Fecha y Hora *
            </label>
            <input
              type="datetime-local"
              id="horario"
              name="horario"
              value={formData.horario}
              onChange={handleChange}
              className={errors.horario ? 'error' : ''}
            />
            {errors.horario && <span className="error-message">{errors.horario}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="equipo_local">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
              </svg>
              Equipo Local *
            </label>
            <select
              id="equipo_local"
              name="equipo_local"
              value={formData.equipo_local}
              onChange={handleChange}
              className={errors.equipo_local ? 'error' : ''}
            >
              <option value="">Seleccionar equipo</option>
              {selecciones.map(seleccion => (
                <option key={seleccion.id_seleccion} value={seleccion.id_seleccion}>
                  {seleccion.pais}
                </option>
              ))}
            </select>
            {errors.equipo_local && <span className="error-message">{errors.equipo_local}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="equipo_visitante">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
              </svg>
              Equipo Visitante *
            </label>
            <select
              id="equipo_visitante"
              name="equipo_visitante"
              value={formData.equipo_visitante}
              onChange={handleChange}
              className={errors.equipo_visitante ? 'error' : ''}
            >
              <option value="">Seleccionar equipo</option>
              {selecciones.map(seleccion => (
                <option key={seleccion.id_seleccion} value={seleccion.id_seleccion}>
                  {seleccion.pais}
                </option>
              ))}
            </select>
            {errors.equipo_visitante && <span className="error-message">{errors.equipo_visitante}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="tipo_partido">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="2" y1="12" x2="22" y2="12"></line>
              </svg>
              Tipo de Partido
            </label>
            <select
              id="tipo_partido"
              name="tipo_partido"
              value={formData.tipo_partido}
              onChange={handleChange}
            >
              <option value="Regular">Regular</option>
              <option value="Octavos de Final">Octavos de Final</option>
              <option value="Cuartos de Final">Cuartos de Final</option>
              <option value="Semifinal">Semifinal</option>
              <option value="Final">Final</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="fk_sede">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                <circle cx="12" cy="10" r="3"></circle>
              </svg>
              Sede (ID)
            </label>
            <input
              type="number"
              id="fk_sede"
              name="fk_sede"
              value={formData.fk_sede}
              onChange={handleChange}
              placeholder="Opcional"
            />
          </div>

          <div className="form-group">
            <label htmlFor="fk_id_fase">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                <polyline points="2 17 12 22 22 17"></polyline>
              </svg>
              Fase (ID)
            </label>
            <input
              type="number"
              id="fk_id_fase"
              name="fk_id_fase"
              value={formData.fk_id_fase}
              onChange={handleChange}
              placeholder="Opcional"
            />
          </div>
        </div>

        <div className="form-section">
          <h3>Resultado (opcional)</h3>
          <div className="resultados-grid">
            <div className="form-group">
              <label htmlFor="gol_local">Goles Local</label>
              <input
                type="number"
                id="gol_local"
                name="gol_local"
                value={formData.gol_local}
                onChange={handleChange}
                min="0"
              />
            </div>
            <div className="form-group">
              <label htmlFor="gol_visitante">Goles Visitante</label>
              <input
                type="number"
                id="gol_visitante"
                name="gol_visitante"
                value={formData.gol_visitante}
                onChange={handleChange}
                min="0"
              />
            </div>
            <div className="form-group">
              <label htmlFor="resultado">Resultado</label>
              <select
                id="resultado"
                name="resultado"
                value={formData.resultado}
                onChange={handleChange}
              >
                <option value="">Sin resultado</option>
                <option value="Local">Victoria Local</option>
                <option value="Visitante">Victoria Visitante</option>
                <option value="Empate">Empate</option>
              </select>
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button type="button" className="cancel-btn" onClick={onCancel}>
            Cancelar
          </button>
          <button type="submit" className="submit-btn">
            {isEditing ? 'Actualizar Partido' : 'Crear Partido'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default FormularioPartido;
