import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import '../estilos/variables.css';
import './PageTransition.css';

const PageTransition = ({ children }) => {
  const location = useLocation();
  const [displayChildren, setDisplayChildren] = useState(children);
  const [transitionStage, setTransitionStage] = useState('fade-in');

  useEffect(() => {
    if (children !== displayChildren) {
      // Etapa de salida
      setTransitionStage('fade-out');
      
      // Cambiar contenido y entrada
      const timer = setTimeout(() => {
        setDisplayChildren(children);
        setTransitionStage('fade-in');
      }, 200); // Reducido de 300ms a 200ms

      return () => clearTimeout(timer);
    }
  }, [children, displayChildren]);

  // Determinar clase adicional según la ruta
  const getRouteClass = () => {
    const path = location.pathname;
    
    if (path === '/login') return 'route-login';
    if (path === '/registro') return 'route-registro';
    if (path === '/panel') return 'route-panel';
    
    return 'route-default';
  };

  return (
    <div className={`page-transition-container ${transitionStage} ${getRouteClass()}`}>
      {displayChildren}
    </div>
  );
};

export default PageTransition;
