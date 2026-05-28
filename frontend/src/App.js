import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ProveedorAutenticacion, useAuth } from './contextos/ContextoAutenticacion';
import { ModulosColorProvider, useModulosColor } from './contextos/ContextoModulos';
import PaginaLogin from './paginas/Login';
import PaginaRegistro from './paginas/Registro';
import RecuperarContrasenaPage from './paginas/RecuperarContrasena';
import { LigasPage, UnirmeLigaPage, LigasPublicasPage } from './paginas/Ligas';
import { PartidosPage } from './paginas/Partidos';
import SeleccionesPage from './paginas/Selecciones';
import JugadoresSeleccionPage from './paginas/Selecciones/JugadoresSeleccionPage';
import HomePage from './paginas/Home/HomePage';
import MarcadorPage from './paginas/Marcador';
import CalendarioPage from './paginas/Calendario/CalendarioPage';
import HistorialPage from './paginas/Historial';
import AdminPage from './paginas/Admin/AdminPage';
import PronosticosPage from './paginas/Pronosticos/PronosticosPage';
import RutaProtegida from './componentes/RutaProtegida';
import PageTransition from './componentes/PageTransition';
import NotificacionesProvider from './componentes/NotificacionesProvider';
import './App.css';

// Componente que aplica el tema automáticamente al cargar
const ThemeInitializer = () => {
  const { aplicarTemaEleganteMundial } = useModulosColor();
  
  React.useEffect(() => {
    // Aplicar el tema elegante automáticamente al cargar la aplicación
    aplicarTemaEleganteMundial();
  }, [aplicarTemaEleganteMundial]);

  return null;
};

function ContenidoApp() {
  const { loading, isAuthenticated } = useAuth();

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
      <Route
        path="/home"
        element={
          <RutaProtegida>
            <HomePage />
          </RutaProtegida>
        }
      />
      <Route path="/login" element={<PaginaLogin />} />
      <Route path="/registro" element={<PaginaRegistro />} />
      <Route path="/recuperar-contrasena" element={<RecuperarContrasenaPage />} />
      <Route path="/GestionLigas" element={
        <RutaProtegida>
          <LigasPage />
        </RutaProtegida>
      } />
      <Route path="/GestionLigas/unirme" element={
        <RutaProtegida>
          <UnirmeLigaPage />
        </RutaProtegida>
      } />
      <Route path="/GestionLigas/publicas" element={
        <RutaProtegida>
          <LigasPublicasPage />
        </RutaProtegida>
      } />
      <Route path="/ligas" element={
        <RutaProtegida>
          <LigasPage />
        </RutaProtegida>
      } />
      <Route path="/partidos" element={
        <RutaProtegida>
          <PartidosPage />
        </RutaProtegida>
      } />
      <Route path="/selecciones" element={
        <RutaProtegida>
          <SeleccionesPage />
        </RutaProtegida>
      } />
      <Route path="/selecciones/:id_seleccion/jugadores" element={
        <RutaProtegida>
          <JugadoresSeleccionPage />
        </RutaProtegida>
      } />
      <Route path="/marcador" element={
        <RutaProtegida>
          <MarcadorPage />
        </RutaProtegida>
      } />
      <Route path="/calendario" element={
        <RutaProtegida>
          <CalendarioPage />
        </RutaProtegida>
      } />
      <Route path="/historial" element={
        <RutaProtegida>
          <HistorialPage />
        </RutaProtegida>
      } />
      <Route path="/pronosticos" element={
        <RutaProtegida>
          <PronosticosPage />
        </RutaProtegida>
      } />
      <Route path="/admin" element={
        <RutaProtegida>
          <AdminPage />
        </RutaProtegida>
      } />
      <Route
        path="/"
        element={<Navigate to={isAuthenticated ? "/home" : "/login"} replace />}
      />
      <Route path="*" element={<Navigate to="/" replace />} />
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
    <ModulosColorProvider>
      <ProveedorAutenticacion>
        <NotificacionesProvider>
          <Router>
            <div className="App">
              <ThemeInitializer />
              <AppWithRouter />
            </div>
          </Router>
        </NotificacionesProvider>
      </ProveedorAutenticacion>
    </ModulosColorProvider>
  );
}

export default App;
