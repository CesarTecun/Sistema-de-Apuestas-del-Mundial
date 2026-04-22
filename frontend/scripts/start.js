#!/usr/bin/env node

// Filtrar advertencias de deprecación antes de iniciar React
const originalEmitWarning = process.emitWarning;

process.emitWarning = (warning, ...args) => {
  if (warning && warning.includes && warning.includes('fs.F_OK is deprecated')) {
    return;
  }
  if (warning && warning.includes && warning.includes('onAfterSetupMiddleware')) {
    return;
  }
  if (warning && warning.includes && warning.includes('onBeforeSetupMiddleware')) {
    return;
  }
  return originalEmitWarning.call(process, warning, ...args);
};

// Iniciar react-app-rewired
require('react-app-rewired/scripts/start');
