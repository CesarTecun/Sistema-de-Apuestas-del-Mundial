import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import FormularioRegistro from './componentes/FormularioRegistro';
import LogoCopaMundial from '../Login/componentes/LogoCopaMundial';
import ModalVideo from '../Login/componentes/ModalVideo';
import './estilos/PaginaRegistro.css';

const PaginaRegistro = () => {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showVideoModal, setShowVideoModal] = useState(false);
  
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

  const handleLogoClick = () => {
    setShowVideoModal(true);
  };

  const handleCloseVideo = () => {
    setShowVideoModal(false);
  };

  return (
    <div className="registro-container">
      <div className="registro-background">
        <div className="registro-form">
          <div className="logo-container">
            <div className="logo logo-clickable">
              <LogoCopaMundial size={150} onClick={handleLogoClick} />
            </div>
          </div>
          
          <FormularioRegistro 
            onSubmit={handleSubmit}
            error={error}
            loading={loading}
          />
        </div>
      </div>
      
      <ModalVideo 
        isOpen={showVideoModal}
        onClose={handleCloseVideo}
        videoId="ct1otkV8iho"
      />
    </div>
  );
};

export default PaginaRegistro;
