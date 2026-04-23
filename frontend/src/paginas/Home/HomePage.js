import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import './estilos/HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 768 && mobileMenuOpen) {
        setMobileMenuOpen(false);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [mobileMenuOpen]);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  return (
    <div className="landing-page">
      {/* Navbar */}
      <nav className="landing-navbar">
        <div className="landing-logo">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
            <path d="M2 12h20"></path>
          </svg>
        </div>
        
        <div className="landing-nav-right">
          <button 
            className="landing-logout-button"
            onClick={handleLogout}
          >
            Cerrar Sesión
          </button>
          <div className="landing-social-icons">
            <a href="#facebook" className="social-icon" aria-label="Facebook">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path>
              </svg>
            </a>
            <a href="#instagram" className="social-icon" aria-label="Instagram">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
              </svg>
            </a>
            <a href="#twitter" className="social-icon" aria-label="Twitter">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path>
              </svg>
            </a>
          </div>
          <button className="landing-menu-button">MENÚ</button>
          <button 
            className="landing-hamburger"
            onClick={toggleMobileMenu}
            aria-label="Menu"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="3" y1="12" x2="21" y2="12"></line>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
          </button>
          <span className="landing-language">ES</span>
        </div>
      </nav>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="landing-mobile-menu">
          <button 
            className="landing-mobile-menu-item"
            onClick={() => {
              handleLogout();
              setMobileMenuOpen(false);
            }}
          >
            Cerrar Sesión
          </button>
        </div>
      )}

      {/* Hero Section */}
      <div className="landing-hero">
        <div className="landing-hero-content">
          <h1 className="landing-title">WORLD CUP 2026</h1>
          <p className="landing-subtitle">Vive la emoción del fútbol como nunca antes</p>
          <button 
            className="landing-cta-button"
            onClick={() => navigate('/GestionLigas')}
          >
            APUESTA AHORA
          </button>
        </div>
        <div className="landing-scroll-indicator">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="2">
            <path d="M7 13l5 5 5-5M7 6l5 5 5-5"></path>
          </svg>
        </div>

        {/* Floating Cards */}
        <div className="landing-cards">
          <div className="landing-card">
            <div className="landing-card-image">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="2" y1="12" x2="22" y2="12"></line>
                <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
              </svg>
            </div>
            <h3 className="landing-card-title">Ligas</h3>
            <p className="landing-card-text">Crea y gestiona tus ligas de apuestas</p>
            <a 
              href="#ligas" 
              className="landing-card-link"
              onClick={(e) => {
                e.preventDefault();
                navigate('/GestionLigas');
              }}
            >
              Ver Ligas →
            </a>
          </div>

          <div className="landing-card">
            <div className="landing-card-image">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="2">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path>
              </svg>
            </div>
            <h3 className="landing-card-title">Partidos</h3>
            <p className="landing-card-text">Explora y gestiona los partidos del Mundial</p>
            <a 
              href="#partidos" 
              className="landing-card-link"
              onClick={(e) => {
                e.preventDefault();
                navigate('/partidos');
              }}
            >
              Ver Partidos →
            </a>
          </div>

          <div className="landing-card">
            <div className="landing-card-image">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="2">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                <path d="M2 12h20"></path>
              </svg>
            </div>
            <h3 className="landing-card-title">Selecciones</h3>
            <p className="landing-card-text">Gestiona las selecciones participantes del Mundial</p>
            <a 
              href="#selecciones" 
              className="landing-card-link"
              onClick={(e) => {
                e.preventDefault();
                navigate('/selecciones');
              }}
            >
              Ver Selecciones →
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
