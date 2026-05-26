import { useEffect } from 'react';
import axios from 'axios';
import { useNotificacionesGlobal } from './NotificacionesProvider';

const TRADUCCIONES = {
  email: 'Correo electrónico',
  password: 'Contraseña',
  password2: 'Confirmar contraseña',
  primer_nombre: 'Primer nombre',
  primer_apellido: 'Primer apellido',
  segundo_nombre: 'Segundo nombre',
  segundo_apellido: 'Segundo apellido',
  telefono: 'Teléfono',
  fecha_nacimiento: 'Fecha de nacimiento',
  nombre_liga: 'Nombre de la liga',
  tipo_liga: 'Tipo de liga',
  estado: 'Estado',
  fk_id_liga: 'Liga',
  horario: 'Fecha y hora',
  equipo_local: 'Equipo local',
  equipo_visitante: 'Equipo visitante',
  monto_total_recaudado: 'Monto total recaudado',
};

function extraerMensajeError(data) {
  if (!data) return 'La información enviada no es válida. Revisa los campos e intenta de nuevo.';
  const campos = Object.keys(data).filter((k) => k !== 'detail' && k !== 'message' && Array.isArray(data[k]));
  if (campos.length > 0) {
    const campo = campos[0];
    const mensajeCampo = data[campo][0];
    const nombreCampo = TRADUCCIONES[campo] || campo.replace(/_/g, ' ');
    return `${nombreCampo}: ${mensajeCampo}`;
  }
  if (data.non_field_errors?.length) return data.non_field_errors[0];
  if (data.detail) return data.detail;
  if (data.message) return data.message;
  return 'La información enviada no es válida. Revisa los campos e intenta de nuevo.';
}

function manejarError({ status, data, url }, { error, warning }) {
  let message = 'Ocurrió un error inesperado';

  if (status === 400) {
    message = extraerMensajeError(data);
    error(message);
  } else if (status === 401) {
    message = 'Tu sesión ha expirado o las credenciales son incorrectas. Por favor inicia sesión de nuevo.';
    error(message);
  } else if (status === 403) {
    message = 'No tienes permisos para realizar esta acción.';
    error(message);
  } else if (status === 404) {
    message = 'El recurso solicitado no fue encontrado.';
    error(message);
  } else if (status === 409) {
    message = data?.detail || data?.message || 'Ya existe un recurso con esa información.';
    warning(message);
  } else if (status >= 500) {
    message = 'Error del servidor. Intenta más tarde o contacta al administrador.';
    error(message);
  } else {
    message = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.';
    error(message);
  }
}

function manejarExito({ status, method, url }, { success }) {
  if (status < 200 || status >= 300) return;
  const m = method?.toLowerCase();
  if (m === 'get') return;

  if (m === 'post') {
    if (url.includes('/auth/register/')) success('Usuario registrado exitosamente');
    else if (url.includes('/ligas/')) success('Liga guardada exitosamente');
    else if (url.includes('/partidos/')) success('Partido guardado exitosamente');
    else if (url.includes('/solicitar-ingreso/') || url.includes('/invitaciones/')) success('Solicitud procesada exitosamente');
  } else if (m === 'put' || m === 'patch') {
    if (url.includes('/ligas/')) success('Liga actualizada exitosamente');
    else if (url.includes('/partidos/')) success('Partido actualizado exitosamente');
  } else if (m === 'delete') {
    if (url.includes('/ligas/')) success('Liga eliminada exitosamente');
    else if (url.includes('/partidos/')) success('Partido eliminado exitosamente');
  }
}

const NotificacionesAxios = () => {
  const notificaciones = useNotificacionesGlobal();

  useEffect(() => {
    // 1) Interceptor para axios global (usado por ContextoAutenticacion, UnirmeLigaPage, etc.)
    const idGlobal = axios.interceptors.response.use(
      (response) => {
        manejarExito(
          { status: response.status, method: response.config?.method, url: response.config?.url },
          notificaciones
        );
        return response;
      },
      (err) => {
        manejarError(
          { status: err.response?.status, data: err.response?.data, url: err.config?.url },
          notificaciones
        );
        return Promise.reject(err);
      }
    );

    // 2) Eventos de servicioApi (usado por servicioPartidos, servicioLigas, etc.)
    const onApiError = (e) => {
      manejarError(e.detail, notificaciones);
    };
    const onApiSuccess = (e) => {
      manejarExito(e.detail, notificaciones);
    };

    window.addEventListener('api-error', onApiError);
    window.addEventListener('api-success', onApiSuccess);

    return () => {
      axios.interceptors.response.eject(idGlobal);
      window.removeEventListener('api-error', onApiError);
      window.removeEventListener('api-success', onApiSuccess);
    };
  }, [notificaciones]);

  return null;
};

export default NotificacionesAxios;
