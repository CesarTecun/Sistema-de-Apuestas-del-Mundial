import React, { createContext, useContext } from 'react';

// Contexto para cambiar colores de módulos
const ModulosColorContext = createContext();

export const useModulosColor = () => {
  const context = useContext(ModulosColorContext);
  if (!context) {
    throw new Error('useModulosColor must be used within a ModulosColorProvider');
  }
  return context;
};

export const ModulosColorProvider = ({ children }) => {
  // Función para cambiar colores de módulos
  const cambiarColorModulo = (primaryColor, secondaryColor, tertiaryColor) => {
    const root = document.documentElement;
    root.style.setProperty('--modulo-primary', primaryColor);
    root.style.setProperty('--modulo-secondary', secondaryColor);
    root.style.setProperty('--modulo-tertiary', tertiaryColor);
    
    // Crear gradiente dinámico
    const gradient = `linear-gradient(135deg, ${primaryColor} 0%, ${secondaryColor} 50%, ${tertiaryColor} 100%)`;
    root.style.setProperty('--modulo-gradient', gradient);
    
    // Forzar actualización
    setTimeout(() => {
      document.body.classList.add('color-transition');
      void document.body.offsetWidth;
      setTimeout(() => {
        document.body.classList.remove('color-transition');
      }, 50);
    }, 10);
  };

  // Función para aplicar tema elegante inspirado en la imagen (desierto nocturno con estrellas)
  const aplicarTemaEleganteMundial = () => {
    const root = document.documentElement;
    
    // Colores principales inspirados en la imagen del desierto nocturno
    const primaryColor = '#6B46C1';     // Púrpura profundo (cielo nocturno)
    const secondaryColor = '#da94b7b4';   // Rosa vibrante (nebula/estrellas)
    const tertiaryColor = '#4C1D95';    // Púrpura muy oscuro (montañas lejanas)
    const accentColor = '#F472B6';      // Rosa claro (detalles brillantes)
    const surfaceColor = 'rgba(255, 255, 255, 0.08)'; // Superficies translúcidas
    
    // Aplicar variables CSS
    root.style.setProperty('--modulo-primary', primaryColor);
    root.style.setProperty('--modulo-secondary', secondaryColor);
    root.style.setProperty('--modulo-tertiary', tertiaryColor);
    root.style.setProperty('--modulo-accent', accentColor);
    root.style.setProperty('--modulo-surface', surfaceColor);
    
    // Gradientes temáticos
    root.style.setProperty('--theme-gradient', `linear-gradient(135deg, 
      ${primaryColor} 0%, 
      ${secondaryColor} 35%, 
      ${tertiaryColor} 70%, 
      rgba(74, 105, 189, 0.8) 100%
    )`);
    
    // Efectos de iluminación tipo estrellas
    root.style.setProperty('--theme-radial1', `radial-gradient(circle at 20% 50%, 
      rgba(236, 72, 153, 0.3) 0%, 
      transparent 50%
    )`);
    
    root.style.setProperty('--theme-radial2', `radial-gradient(circle at 80% 20%, 
      rgba(244, 114, 182, 0.2) 0%, 
      transparent 50%
    )`);
    
    // Colores para elementos interactivos
    root.style.setProperty('--modulo-button-primary', `linear-gradient(135deg, ${primaryColor} 0%, ${secondaryColor} 100%)`);
    root.style.setProperty('--modulo-button-hover', `linear-gradient(135deg, #7C3AED 0%, #F472B6 100%)`);
    root.style.setProperty('--modulo-input-bg', 'rgba(255, 255, 255, 0.12)');
    root.style.setProperty('--modulo-input-border', 'rgba(255, 255, 255, 0.3)');
    root.style.setProperty('--modulo-text-primary', '#ffffff');
    root.style.setProperty('--modulo-text-secondary', 'rgba(255, 255, 255, 0.8)');
    
    // Sombras y efectos de profundidad
    root.style.setProperty('--modulo-shadow', '0 20px 40px rgba(0, 0, 0, 0.3)');
    root.style.setProperty('--modulo-shadow-button', '0 12px 25px rgba(236, 72, 153, 0.4)');
    
    // Actualizar fondo del body
    document.body.style.background = `linear-gradient(135deg, 
      ${primaryColor} 0%, 
      ${secondaryColor} 35%, 
      ${tertiaryColor} 70%, 
      rgba(74, 105, 189, 0.8) 100%
    )`;
    
    // Forzar transición suave
    setTimeout(() => {
      document.body.classList.add('color-transition');
      void document.body.offsetWidth;
      setTimeout(() => {
        document.body.classList.remove('color-transition');
      }, 50);
    }, 10);
  };

  return (
    <ModulosColorContext.Provider value={{ cambiarColorModulo, aplicarTemaEleganteMundial }}>
      {children}
    </ModulosColorContext.Provider>
  );
};

export default ModulosColorContext;
