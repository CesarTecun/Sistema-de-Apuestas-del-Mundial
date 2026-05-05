import React from 'react';
import './estilos/LandingPage.css';

const LandingPage = () => {
  return (
    <div className="landing-page">
      {/* Navbar */}
      <nav className="landing-navbar">
        <button className="landing-nav-button">Reservar</button>
        
        <div className="landing-logo">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
            <path d="M2 12h20"></path>
          </svg>
        </div>
        
        <div className="landing-nav-right">
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
          <span className="landing-language">ES</span>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="landing-hero">
        <div className="landing-hero-content">
          <h1 className="landing-title">WORLD CUP 2026</h1>
          <p className="landing-subtitle">Vive la emoción del fútbol como nunca antes</p>
        </div>
      </div>

      {/* Floating Cards */}
      <div className="landing-cards">
        <div className="landing-card">
          <div className="landing-card-image">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </div>
          <h3 className="landing-card-title">La pasión del fútbol</h3>
          <p className="landing-card-text">La pasión del fútbol en su máxima expresión</p>
          <a href="#passion" className="landing-card-link">Ver más →</a>
        </div>

        <div className="landing-card">
          <div className="landing-card-image">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="2">
              <path d="M3 21h18M5 21V7l8-4 8 4v14M8 21v-2a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
          </div>
          <h3 className="landing-card-title">Estadios icónicos</h3>
          <p className="landing-card-text">Descubre los estadios más icónicos del Mundial 2026</p>
          <a href="#stadiums" className="landing-card-link">Ver más →</a>
        </div>

        <div className="landing-card">
          <div className="landing-card-image">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="2">
              <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
              <line x1="1" y1="10" x2="23" y2="10"></line>
            </svg>
          </div>
          <h3 className="landing-card-title">Compra tus entradas</h3>
          <p className="landing-card-text">Compra tus entradas y asegura tu lugar</p>
          <a href="#tickets" className="landing-card-link">Ver más →</a>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
