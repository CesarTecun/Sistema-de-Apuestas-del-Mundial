import React, { useState, useEffect } from 'react';
import '../estilos/FormularioPartido.css';

const FormularioPartido = ({ onSubmit, onCancel, initialData, isEditing, selecciones, ligas = [], sedes = [], defaultLigaId }) => {
  const [formData, setFormData] = useState({
    horario: '',
    equipo_local: '',
    equipo_visitante: '',
    ciudad_sede: '',
    fk_id_fase: '',
    fk_id_liga: '',
    tipo_partido: 'Regular',
    gol_local: 0,
    gol_visitante: 0,
    resultado: ''
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (initialData) {
      // Si estamos editando, necesitamos encontrar la ciudad correspondiente al fk_sede
      const sede = sedes.find(s => s.id_sede === initialData.fk_sede);
      setFormData({
        horario: initialData.horario || '',
        equipo_local: initialData.equipo_local || '',
        equipo_visitante: initialData.equipo_visitante || '',
        ciudad_sede: sede ? sede.ciudad : '',
        fk_id_fase: initialData.fk_id_fase || '',
        fk_id_liga: initialData.fk_id_liga || defaultLigaId || '',
        tipo_partido: initialData.tipo_partido || 'Regular',
        gol_local: initialData.gol_local || 0,
        gol_visitante: initialData.gol_visitante || 0,
        resultado: initialData.resultado || ''
      });
    } else if (defaultLigaId) {
      setFormData((prev) => ({
        ...prev,
        fk_id_liga: defaultLigaId,
      }));
    }
  }, [initialData, defaultLigaId, sedes]);

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

    if (!formData.fk_id_liga) {
      newErrors.fk_id_liga = 'Debes seleccionar la liga a la que pertenece el partido';
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
        fk_id_liga: parseInt(formData.fk_id_liga),
        ciudad_sede: formData.ciudad_sede || null,
        fk_id_fase: formData.fk_id_fase ? parseInt(formData.fk_id_fase) : null
      };
      // Eliminar fk_sede ya que ahora enviamos ciudad_sede
      delete dataToSubmit.fk_sede;
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
            <label htmlFor="fk_id_liga">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
              </svg>
              Liga *
            </label>
            <select
              id="fk_id_liga"
              name="fk_id_liga"
              value={formData.fk_id_liga}
              onChange={handleChange}
              className={errors.fk_id_liga ? 'error' : ''}
            >
              <option value="">Seleccionar liga</option>
              {ligas.map((liga) => (
                <option key={liga.id_liga} value={liga.id_liga}>
                  {liga.nombre_liga}
                </option>
              ))}
            </select>
            {errors.fk_id_liga && <span className="error-message">{errors.fk_id_liga}</span>}
          </div>

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
              Fases de Partido
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
            <label htmlFor="ciudad_sede">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                <circle cx="12" cy="10" r="3"></circle>
              </svg>
              Sede (Ciudad)
            </label>
            <select
              id="ciudad_sede"
              name="ciudad_sede"
              value={formData.ciudad_sede}
              onChange={handleChange}
            >
              <option value="">Seleccionar sede</option>
              {sedes.map((sede) => (
                <option key={sede.id_sede} value={sede.ciudad}>
                  {sede.ciudad} - {sede.estadio}
                </option>
              ))}
            </select>
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
