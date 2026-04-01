import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import FormularioLogin from './componentes/FormularioLogin';
import LogoCopaMundial from './componentes/LogoCopaMundial';
import ModalVideo from './componentes/ModalVideo';
import './estilos/PaginaLogin.css';
import './estilos/LoginSpecific.css';

const PaginaLogin = () => {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showVideoModal, setShowVideoModal] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (formData) => {
    setError('');
    setLoading(true);

    const result = await login(formData.email, formData.password);
    
    if (result.success) {
      navigate('/panel');
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
    <div className="login-page login-container">
      <div className="login-background">
        <div className="login-form">
          <div className="logo-container">
            <div className="logo">
              <LogoCopaMundial size={300} onClick={handleLogoClick} />
            </div>
          </div>
          
          <FormularioLogin 
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

export default PaginaLogin;