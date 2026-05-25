import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API_ENDPOINTS } from '../../config/apiConfig';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import TopBar from './componentes/TopBar';
import useNotificaciones from '../../hooks/useNotificaciones';
import NotificacionesContainer from '../../componentes/NotificacionesContainer';
import './estilos/LigasPublicasPage.css';

const LigasPublicasPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { notificaciones, cerrarNotificacion, error: mostrarError } = useNotificaciones();

  const [ligas, setLigas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [tipo, setTipo] = useState('');
  const [requiereAprobacion, setRequiereAprobacion] = useState('');
  const [soloDisponibles, setSoloDisponibles] = useState(true);

  const debouncedSearch = useMemo(() => search.trim(), [search]);

  const handleLogout = async () => {
    await logout();
    navigate('/home');
  };

  useEffect(() => {
    const controller = new AbortController();
    const fetchLigas = async () => {
      try {
        setLoading(true);
        const response = await axios.get(API_ENDPOINTS.LIGAS_PUBLICAS, {
          params: {
            search: debouncedSearch || undefined,
            tipo: tipo || undefined,
            requiere_aprobacion: requiereAprobacion || undefined,
            disponibles: soloDisponibles ? 'true' : undefined,
          },
          signal: controller.signal,
        });
        setLigas(response.data?.results || []);
      } catch (error) {
        if (!axios.isCancel(error)) {
          console.error('Error al cargar ligas públicas', error);
          mostrarError('No pudimos cargar la lista pública de ligas en este momento.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchLigas();
    return () => controller.abort();
  }, [debouncedSearch, tipo, requiereAprobacion, soloDisponibles, mostrarError]);

  return (
    <div className="ligas-container no-animation">
      <div className="ligas-background">
        <div className="ligas-wrapper">
          <TopBar user={user} onLogout={handleLogout} />

          <div className="publicas-card">
            <header className="join-header">
              <div>
                <p className="eyebrow">Explorar</p>
                <h1>Ligas públicas</h1>
                <p>Consulta qué ligas tienen cupo disponible y solicita acceso desde la pantalla principal.</p>
              </div>
            </header>

            <div className="publicas-filtros">
              <input
                type="text"
                placeholder="Buscar por nombre o descripción"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
              <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
                <option value="">Todos los tipos</option>
                <option value="Diversion">Diversión</option>
                <option value="Competitiva">Competitiva</option>
              </select>
              <select value={requiereAprobacion} onChange={(e) => setRequiereAprobacion(e.target.value)}>
                <option value="">Cualquier aprobación</option>
                <option value="true">Requiere aprobación</option>
                <option value="false">Ingreso automático</option>
              </select>
              <label className="checkbox">
                <input
                  type="checkbox"
                  checked={soloDisponibles}
                  onChange={(e) => setSoloDisponibles(e.target.checked)}
                />
                Mostrar solo con cupos
              </label>
            </div>

            <div className="public-list">
              {loading && <p className="helper-text">Cargando ligas...</p>}
              {!loading && ligas.length === 0 && <p className="helper-text">No hay ligas con estos filtros.</p>}

              {ligas.map((liga) => (
                <article className="public-card" key={liga.id_liga}>
                  <div className="public-card__body">
                    <div>
                      <h4>{liga.nombre_liga}</h4>
                      <p>{liga.descripcion || 'Sin descripción'}</p>
                    </div>
                    <ul>
                      <li>
                        <span>Cupo:</span>
                        <strong>
                          {liga.cupo_maximo == null
                            ? 'Ilimitado'
                            : `${liga.total_participantes}/${liga.cupo_maximo}`}
                        </strong>
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
                    <button onClick={() => navigate('/GestionLigas/unirme', { state: { codigoLiga: liga.codigo_invitacion } })}>
                      Solicitar acceso
                    </button>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </div>

        <NotificacionesContainer notificaciones={notificaciones} onClose={cerrarNotificacion} />
      </div>
    </div>
  );
};

export default LigasPublicasPage;
