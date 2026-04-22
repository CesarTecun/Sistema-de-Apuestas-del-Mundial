module.exports = {
  webpack: (config, { env }) => {
    // Eliminar todas las advertencias de deprecación
    config.ignoreWarnings = [
      /fs\.F_OK is deprecated/,
      /onAfterSetupMiddleware/,
      /onBeforeSetupMiddleware/,
      /DEP0176/,
    ];
    
    return config;
  },
  devServer: (configFunction) => {
    return (proxy, allowedHost) => {
      const config = configFunction(proxy, allowedHost);
      
      // Eliminar opciones deprecadas
      delete config.onAfterSetupMiddleware;
      delete config.onBeforeSetupMiddleware;
      
      return config;
    };
  },
};
