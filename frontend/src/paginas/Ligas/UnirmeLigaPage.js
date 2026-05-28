import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API_ENDPOINTS, getAuthHeaders } from '../../config/apiConfig';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import useNotificaciones from '../../hooks/useNotificaciones';
import NotificacionesContainer from '../../componentes/NotificacionesContainer';
import TopBar from './componentes/TopBar';
import './estilos/UnirmeLigaPage.css';

const initialFeedback = { status: 'idle', message: '' };

const UnirmeLigaPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const {
    notificaciones,
    success,
    error: mostrarError,
    cerrarNotificacion,
  } = useNotificaciones();

  const [publicLeagues, setPublicLeagues] = useState([]);
  const [publicLoading, setPublicLoading] = useState(false);
  const [publicSearch, setPublicSearch] = useState('');
  const [solicitudes, setSolicitudes] = useState({});

  const [codigo, setCodigo] = useState('');
  const [codigoFeedback, setCodigoFeedback] = useState(initialFeedback);
  const [codigoLoading, setCodigoLoading] = useState(false);

  const debouncedSearch = useMemo(() => publicSearch.trim().toLowerCase(), [publicSearch]);

  const handleLogout = async () => {
    await logout();
    navigate('/home');
  };

  useEffect(() => {
    const controller = new AbortController();

    const fetchPublicLeagues = async () => {
      try {
        console.log('[UnirmeLigaPage] Fetching public leagues from:', API_ENDPOINTS.LIGAS_PUBLICAS);
        setPublicLoading(true);
        const response = await axios.get(API_ENDPOINTS.LIGAS_PUBLICAS, {
          params: {
            search: debouncedSearch || undefined,
            disponibles: 'true',
          },
          signal: controller.signal,
        });
        console.log('[UnirmeLigaPage] Public leagues response:', response.data);
        setPublicLeagues(response.data?.results || []);
      } catch (error) {
        if (!axios.isCancel(error)) {
          console.error('[UnirmeLigaPage] Error al cargar ligas públicas', error);
          console.error('[UnirmeLigaPage] Error response:', error.response);
          console.error('[UnirmeLigaPage] Error message:', error.message);
          mostrarError('No pudimos cargar las ligas públicas en este momento.');
        }
      } finally {
        setPublicLoading(false);
      }
    };

    fetchPublicLeagues();
    return () => controller.abort();
  }, [debouncedSearch, mostrarError]);

  const solicitarIngreso = async (liga) => {
    if (!liga) return;

    try {
      const response = await axios.post(
        API_ENDPOINTS.LIGA_SOLICITAR_INGRESO(liga.id_liga),
        {},
        { headers: getAuthHeaders() }
      );

      setSolicitudes((prev) => ({
        ...prev,
        [liga.id_liga]: response.data?.aprobacion_requerida ? 'pendiente' : 'aceptado',
      }));

      // success(response.data?.message || 'Solicitud enviada correctamente.');
      if (!response.data?.aprobacion_requerida) {
        navigate('/GestionLigas');
      }
    } catch (error) {
      const message =
        error.response?.data?.error ||
        error.response?.data?.message ||
        'No pudimos enviar tu solicitud en este momento.';
      mostrarError(message);
    }
  };

  const handleCodigoSubmit = async (event) => {
    event.preventDefault();
    if (!codigo.trim()) return;

    setCodigoLoading(true);
    setCodigoFeedback(initialFeedback);

    try {
      const codigoNormalizado = codigo.trim();
      const detalle = await axios.get(API_ENDPOINTS.INVITACION_PUBLICA(codigoNormalizado));

      if (detalle.data?.estado !== 'Pendiente') {
        throw new Error('Esta invitación ya fue gestionada.');
      }

      await axios.post(
        API_ENDPOINTS.INVITACION_PUBLICA(codigoNormalizado),
        { email: user?.email },
        { headers: getAuthHeaders() }
      );

      setCodigo('');
      setCodigoFeedback({ status: 'success', message: 'Invitación aceptada. Ya formas parte de la liga.' });
      // success('Invitación aceptada correctamente.');
      navigate('/GestionLigas');
    } catch (error) {
      const message =
        error.response?.data?.error ||
        error.response?.data?.message ||
        error.response?.data?.detail ||
        error.message ||
        'No pudimos validar el código ingresado.';
      setCodigoFeedback({ status: 'error', message });
      mostrarError(message);
    } finally {
      setCodigoLoading(false);
    }
  };

  return (
    <div className="ligas-container no-animation">
      <div className="ligas-background">
        <div className="ligas-wrapper">
          <TopBar user={user} onLogout={handleLogout} />

          <div className="join-card">
            <header className="join-header">
              <div>
                <p className="eyebrow">Unirme a una liga</p>
                <h1>Solicitud de acceso</h1>
                <p>
                  Explora ligas públicas disponibles o ingresa un código de invitación compartido por un administrador.
                </p>
              </div>
              <div className="join-hint">
                Estás autenticado como <strong>{user?.email}</strong>. Utilizaremos este correo para vincular tu participación.
              </div>
            </header>

            <div className="join-grid">
              <section className="panel">
                <div className="panel__header">
                  <div>
                    <h2>Ligas públicas</h2>
                    <p>Solicita un cupo en ligas abiertas a la comunidad.</p>
                  </div>
                  <div className="tag tag--outline">Solicitud enviada ≠ ingreso inmediato</div>
                </div>

                <div className="public-search">
                  <input
                    type="text"
                    placeholder="Buscar por nombre, tipo o descripción..."
                    value={publicSearch}
                    onChange={(event) => setPublicSearch(event.target.value)}
                  />
                </div>

                <div className="public-list">
                  {publicLoading && <p className="helper-text">Buscando ligas disponibles...</p>}

                  {!publicLoading && publicLeagues.length === 0 && (
                    <p className="helper-text">No encontramos ligas públicas con esos criterios.</p>
                  )}

                  {!publicLoading &&
                    publicLeagues.map((liga) => {
                      const estadoSolicitud = solicitudes[liga.id_liga];
                      const cupoTexto =
                        liga.cupo_maximo == null
                          ? 'Cupo ilimitado'
                          : `${liga.total_participantes}/${liga.cupo_maximo} participantes`;

                      return (
                        <article className="public-card" key={liga.id_liga}>
                          <div className="public-card__body">
                            <div>
                              <h4>{liga.nombre_liga}</h4>
                              <p>{liga.descripcion || 'Sin descripción disponible.'}</p>
                            </div>
                            <ul>
                              <li>
                                <span>Cupo:</span>
                                <strong>{cupoTexto}</strong>
                              </li>
                              <li>
                                <span>Tipo:</span>
                                <strong>{liga.tipo_liga}</strong>
                              </li>
                              <li>
                                <span>Requiere aprobación:</span>
                                <strong>{liga.requiere_aprobacion ? 'Sí' : 'No'}</strong>
                              </li>
                            </ul>
                          </div>
                          <div className="public-card__actions">
                            {estadoSolicitud ? (
                              <span className={`tag ${estadoSolicitud === 'aceptado' ? 'tag--success' : 'tag--warning'}`}>
                                {estadoSolicitud === 'aceptado' ? 'Ingreso confirmado' : 'Solicitud enviada'}
                              </span>
                            ) : (
                              <button onClick={() => solicitarIngreso(liga)}>Solicitar acceso</button>
                            )}
                          </div>
                        </article>
                      );
                    })}
                </div>
              </section>

              <section className="panel">
                <div className="panel__header">
                  <div>
                    <h2>Tengo un código</h2>
                    <p>Introduce el código que recibiste por correo para ingresar de inmediato.</p>
                  </div>
                </div>

                <form className="codigo-form" onSubmit={handleCodigoSubmit}>
                  <label htmlFor="codigo">Código de invitación</label>
                  <input
                    id="codigo"
                    type="text"
                    value={codigo}
                    onChange={(event) => setCodigo(event.target.value)}
                    placeholder="Ej. 00565404-37a1-4ea4-919a-d3c08f0b01a"
                    required
                  />
                  <p className="helper-text">
                    Puedes encontrarlo en el correo de invitación. Si no tienes cuenta, crea una desde la pantalla de inicio de sesión antes de usarlo.
                  </p>

                  {codigoFeedback.status !== 'idle' && (
                    <div className={`codigo-feedback codigo-feedback--${codigoFeedback.status}`}>
                      {codigoFeedback.message}
                    </div>
                  )}

                  <button type="submit" className="submit" disabled={codigoLoading}>
                    {codigoLoading ? 'Validando...' : 'Unirme con código'}
                  </button>
                </form>
              </section>
            </div>
          </div>
        </div>

        <NotificacionesContainer notificaciones={notificaciones} onClose={cerrarNotificacion} />
      </div>
    </div>
  );
};

export default UnirmeLigaPage;
