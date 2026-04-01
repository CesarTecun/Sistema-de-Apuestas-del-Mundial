import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import FormularioRegistro from './componentes/FormularioRegistro';
import LogoCopaMundial from '../Login/componentes/LogoCopaMundial';
import './estilos/PaginaRegistro.css';

const PaginaRegistro = () => {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (formData) => {
    setError('');
    setLoading(true);

    const result = await register(formData);
    
    if (result.success) {
      navigate('/login');
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <div className="registro-container">
      <div className="registro-background">
        <div className="registro-form">
          <div className="logo-container">
            <div className="logo">
              <LogoCopaMundial size={300} />
            </div>
          </div>
          
          <FormularioRegistro 
            onSubmit={handleSubmit}
            error={error}
            loading={loading}
          />
        </div>
      </div>
    </div>
  );
};

export default PaginaRegistro;
