import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ProveedorAutenticacion, useAuth } from './contextos/ContextoAutenticacion';
import PaginaLogin from './paginas/Login';
import PaginaRegistro from './paginas/Registro';
import PanelPrincipal from './paginas/Panel';
import RutaProtegida from './componentes/RutaProtegida';
import PageTransition from './componentes/PageTransition';
import './App.css';

function ContenidoApp() {
  const { loading } = useAuth();

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        fontSize: '18px',
        background: 'linear-gradient(135deg, rgba(168, 50, 121, 0.8) 0%, rgba(106, 76, 147, 0.8) 100%)',
        color: 'white'
      }}>
        <div>
          <div style={{ 
            width: '40px', 
            height: '40px', 
            border: '3px solid rgba(255, 255, 255, 0.3)',
            borderTop: '3px solid #ffffff',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 20px'
          }}></div>
          Cargando...
        </div>
      </div>
    );
  }

  return (
    <Routes>
      <Route path="/login" element={<PaginaLogin />} />
      <Route path="/registro" element={<PaginaRegistro />} />
      <Route path="/panel" element={
        <RutaProtegida>
          <PanelPrincipal />
        </RutaProtegida>
      } />
      <Route path="/" element={<Navigate to="/panel" replace />} />
    </Routes>
  );
}

function AppWithRouter() {
  return (
    <PageTransition>
      <ContenidoApp />
    </PageTransition>
  );
}

function App() {
  return (
    <ProveedorAutenticacion>
      <Router>
        <div className="App">
          <AppWithRouter />
        </div>
      </Router>
    </ProveedorAutenticacion>
  );
}

export default App;
