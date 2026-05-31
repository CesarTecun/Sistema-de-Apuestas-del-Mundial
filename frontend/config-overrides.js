module.exports = {
  webpack: (config, { env }) => {
    // Eliminar todas las advertencias de deprecación
    config.ignoreWarnings = [
      /fs\.F_OK is deprecated/,
      /onAfterSetupMiddleware/,
      /onBeforeSetupMiddleware/,
      /DEP0176/,
    ];

    // Deshabilitar hot-reload en producción
    if (env === 'production') {
      config.target = 'web';
      // Eliminar plugins de hot-reload en producción
      config.plugins = config.plugins.filter(plugin => {
        return plugin.constructor.name !== 'HotModuleReplacementPlugin';
      });
    }

    return config;
  },
  devServer: (configFunction) => {
    return (proxy, allowedHost) => {
      const config = configFunction(proxy, allowedHost);

      // Eliminar opciones deprecadas
      delete config.onAfterSetupMiddleware;
      delete config.onBeforeSetupMiddleware;

      // Deshabilitar hot-reload en producción
      if (process.env.NODE_ENV === 'production') {
        config.hot = false;
        config.liveReload = false;
      }

      return config;
    };
  },
};
