import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contextos/ContextoAutenticacion';
import useNotificaciones from '../../hooks/useNotificaciones';
import NotificacionesContainer from '../../componentes/NotificacionesContainer';
import servicioApi from '../../servicios/servicioApi';
import './estilos/AdminPage.css';

// ── Icons ────────────────────────────────────────────────────────────────────

const icons = {
  dashboard: "M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z",
  users:     "M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm14 10v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75",
  config:    "M12 20h9M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z",
  bitacora:  "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z",
  auditlog:  "M9 11l3 3L22 4M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11",
  back:      "M15 18l-6-6 6-6",
  logout:    "M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4 M16 17l5-5-5-5 M21 12H9",
  refresh:   "M23 4v6h-6 M1 20v-6h6 M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15",
  user:      "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2 M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8",
  check:     "M20 6L9 17l-5-5",
  x:         "M18 6L6 18M6 6l12 12",
};

const MultiPathIcon = ({ paths, size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
    stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    {paths.map((d, i) => <path key={i} d={d} />)}
  </svg>
);

// ── Helpers ──────────────────────────────────────────────────────────────────

const fmt = (n) => (n ?? 0).toLocaleString();
const fmtMoney = (n) => `Q ${(n ?? 0).toLocaleString('es-GT', { minimumFractionDigits: 2 })}`;
const fmtDate = (d) => d ? new Date(d).toLocaleDateString('es-GT') : '—';
const fmtDatetime = (d) => d ? new Date(d).toLocaleString('es-GT') : '—';

// ── TOP BAR ──────────────────────────────────────────────────────────────────

const AdminTopBar = ({ user, onBack, onLogout }) => (
  <div className="top-bar">
    <div className="top-bar-left">
      <button 
        className="back-button"
        onClick={onBack}
        aria-label="Volver"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
        <span>Volver</span>
      </button>
    </div>

    <div className="user-info">
      <div className="user-avatar">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>
      </div>
      <div className="user-details">
        <span className="user-name">
          {user?.primer_nombre} {user?.primer_apellido}
        </span>
        <span className="user-email">{user?.email}</span>
      </div>
    </div>
    
    <div className="top-bar-actions">
      <button 
        className="logout-button"
        onClick={onLogout}
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
        Cerrar Sesión
      </button>
    </div>
  </div>
);

// ── DASHBOARD ────────────────────────────────────────────────────────────────

const StatCard = ({ icon, iconClass, label, value, sub }) => (
  <div className="stat-card">
    <div className="stat-card-header">
      <div className={`stat-card-icon ${iconClass}`}>{icon}</div>
      <span className="stat-card-label">{label}</span>
    </div>
    <div className="stat-card-value">{value}</div>
    {sub && <div className="stat-card-sub">{sub}</div>}
  </div>
);

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const cargar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await servicioApi.get('/core/reportes/resumen/');
      setData(res.data);
    } catch (e) {
      setError('No se pudo cargar el resumen. Verifica tu conexión.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { cargar(); }, [cargar]);

  if (loading) return (
    <div className="admin-loading">
      <div className="admin-spinner" />
      <span>Cargando resumen...</span>
    </div>
  );

  if (error) return (
    <div>
      <div className="admin-error-msg">{error}</div>
      <button className="btn-refresh" onClick={cargar}>
        <MultiPathIcon paths={[icons.refresh]} size={14} /> Reintentar
      </button>
    </div>
  );

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 'var(--spacing-md)' }}>
        <button className="btn-refresh" onClick={cargar}>
          <MultiPathIcon paths={[icons.refresh]} size={14} /> Actualizar
        </button>
      </div>

      <p className="stats-section-title">Usuarios</p>
      <div className="stats-grid">
        <StatCard iconClass="purple" icon={<MultiPathIcon paths={[icons.users]} size={22} />}
          label="Total usuarios" value={fmt(data?.usuarios?.total)}
          sub={`${fmt(data?.usuarios?.admins)} administradores`} />
        <StatCard iconClass="green" icon={<MultiPathIcon paths={[icons.check]} size={22} />}
          label="Activos" value={fmt(data?.usuarios?.activos)} />
        <StatCard iconClass="red" icon={<MultiPathIcon paths={[icons.x]} size={22} />}
          label="Inactivos" value={fmt(data?.usuarios?.inactivos)} />
        <StatCard iconClass="blue" icon={<MultiPathIcon paths={[icons.user]} size={22} />}
          label="Sesiones activas" value={fmt(data?.sesiones?.activas_ahora)} />
      </div>

      <p className="stats-section-title">Ligas</p>
      <div className="stats-grid">
        <StatCard iconClass="purple" icon={<MultiPathIcon paths={[icons.dashboard]} size={22} />}
          label="Total ligas" value={fmt(data?.ligas?.total)} />
        <StatCard iconClass="green" icon={<MultiPathIcon paths={[icons.check]} size={22} />}
          label="Activas" value={fmt(data?.ligas?.activas)} />
        <StatCard iconClass="blue" icon={<MultiPathIcon paths={[icons.users]} size={22} />}
          label="Públicas" value={fmt(data?.ligas?.publicas)} />
        <StatCard iconClass="gold" icon={<MultiPathIcon paths={[icons.config]} size={22} />}
          label="Competitivas" value={fmt(data?.ligas?.competitivas)} />
      </div>

      <p className="stats-section-title">Partidos</p>
      <div className="stats-grid">
        <StatCard iconClass="blue" icon={<MultiPathIcon paths={[icons.dashboard]} size={22} />}
          label="Total" value={fmt(data?.partidos?.total)} />
        <StatCard iconClass="warning" icon={<MultiPathIcon paths={[icons.config]} size={22} />}
          label="Programados" value={fmt(data?.partidos?.programados)} />
        <StatCard iconClass="green" icon={<MultiPathIcon paths={[icons.check]} size={22} />}
          label="En juego" value={fmt(data?.partidos?.en_juego)} />
        <StatCard iconClass="teal" icon={<MultiPathIcon paths={[icons.check]} size={22} />}
          label="Finalizados" value={fmt(data?.partidos?.finalizados)} />
      </div>

      <p className="stats-section-title">Finanzas</p>
      <div className="stats-grid">
        <StatCard iconClass="gold" icon={<MultiPathIcon paths={[icons.config]} size={22} />}
          label="Pronósticos" value={fmt(data?.pronosticos?.total)} />
        <StatCard iconClass="purple" icon={<MultiPathIcon paths={[icons.config]} size={22} />}
          label="Total recaudado" value={fmtMoney(data?.premios?.total_recaudado)} />
        <StatCard iconClass="green" icon={<MultiPathIcon paths={[icons.config]} size={22} />}
          label="Total distribuido" value={fmtMoney(data?.premios?.total_distribuido)} />
      </div>

      <p style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-muted)', marginTop: 'var(--spacing-lg)' }}>
        Generado: {fmtDatetime(data?.generado_en)}
      </p>
    </div>
  );
};

// ── GESTIÓN DE USUARIOS ───────────────────────────────────────────────────────

const GestionUsuarios = ({ notif }) => {
  const { user } = useAuth();
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [filtroRol, setFiltroRol] = useState('');
  const [filtroActivo, setFiltroActivo] = useState('');
  const [accionando, setAccionando] = useState(null);

  const cargar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = {};
      if (search) params.search = search;
      if (filtroRol) params.fk_rol = filtroRol;
      if (filtroActivo !== '') params.activo = filtroActivo;
      const res = await servicioApi.get('/usuarios/', { params });
      const data = res.data;
      setUsuarios(Array.isArray(data) ? data : (data.results ?? []));
    } catch {
      setError('No se pudo cargar la lista de usuarios.');
    } finally {
      setLoading(false);
    }
  }, [search, filtroRol, filtroActivo]);

  useEffect(() => {
    const t = setTimeout(() => cargar(), 350);
    return () => clearTimeout(t);
  }, [cargar]);

  const activar = async (id) => {
    setAccionando(id);
    try {
      await servicioApi.post(`/usuarios/${id}/activar/`);
      notif.success('Usuario activado correctamente');
      cargar();
    } catch {
      notif.error('Error al activar usuario');
    } finally {
      setAccionando(null);
    }
  };

  const desactivar = async (id) => {
    if (id === user?.id_usuario) {
      notif.error('No puedes desactivar tu propio usuario');
      return;
    }
    setAccionando(id);
    try {
      await servicioApi.post(`/usuarios/${id}/desactivar/`);
      notif.success('Usuario desactivado correctamente');
      cargar();
    } catch {
      notif.error('Error al desactivar usuario');
    } finally {
      setAccionando(null);
    }
  };

  return (
    <div>
      <div className="admin-filters">
        <input className="admin-search-input" placeholder="Buscar por nombre o email..."
          value={search} onChange={e => setSearch(e.target.value)} />
        <select className="admin-select" value={filtroRol} onChange={e => setFiltroRol(e.target.value)}>
          <option value="">Todos los roles</option>
          <option value="1">Administrador</option>
          <option value="2">Usuario</option>
        </select>
        <select className="admin-select" value={filtroActivo} onChange={e => setFiltroActivo(e.target.value)}>
          <option value="">Todos los estados</option>
          <option value="true">Activos</option>
          <option value="false">Inactivos</option>
        </select>
        <button className="btn-refresh" onClick={cargar}>
          <MultiPathIcon paths={[icons.refresh]} size={14} /> Actualizar
        </button>
      </div>

      {error && <div className="admin-error-msg">{error}</div>}

      {loading ? (
        <div className="admin-loading">
          <div className="admin-spinner" />
          <span>Cargando usuarios...</span>
        </div>
      ) : usuarios.length === 0 ? (
        <div className="admin-empty">
          <MultiPathIcon paths={[icons.users]} size={48} />
          <p>No se encontraron usuarios</p>
        </div>
      ) : (
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Nombre</th>
                <th>Email</th>
                <th>Rol</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {usuarios.map(u => (
                <tr key={u.id_usuario}>
                  <td style={{ color: 'var(--text-muted)' }}>{u.id_usuario}</td>
                  <td>{u.nombre_completo || `${u.primer_nombre} ${u.primer_apellido}`}</td>
                  <td style={{ color: 'var(--text-tertiary)' }}>{u.email}</td>
                  <td>
                    <span className={`badge ${u.fk_rol === 1 ? 'badge-gold' : 'badge-info'}`}>
                      {u.fk_rol === 1 ? 'Admin' : 'Usuario'}
                    </span>
                  </td>
                  <td>
                    <span className={`badge ${u.status ? 'badge-success' : 'badge-danger'}`}>
                      {u.status ? 'Activo' : 'Inactivo'}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '6px' }}>
                      {!u.status ? (
                        <button className="btn-action btn-activate"
                          disabled={accionando === u.id_usuario}
                          onClick={() => activar(u.id_usuario)}>
                          <MultiPathIcon paths={[icons.check]} size={12} />
                          Activar
                        </button>
                      ) : (
                        <button className="btn-action btn-deactivate"
                          disabled={accionando === u.id_usuario || u.id_usuario === user?.id_usuario}
                          onClick={() => desactivar(u.id_usuario)}
                          title={u.id_usuario === user?.id_usuario ? 'No puedes desactivar tu propio usuario' : ''}>
                          <MultiPathIcon paths={[icons.x]} size={12} />
                          Desactivar
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="admin-table-footer">
            {usuarios.length} usuario(s) encontrado(s)
          </div>
        </div>
      )}
    </div>
  );
};

// ── CONFIGURACIÓN DEL TORNEO ─────────────────────────────────────────────────

const ConfiguracionTorneo = ({ notif }) => {
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const cargar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await servicioApi.get('/core/configuracion/');
      setConfig(res.data);
    } catch {
      setError('No se pudo cargar la configuración.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { cargar(); }, [cargar]);

  const handleChange = (field, value) => {
    setConfig(prev => ({ ...prev, [field]: value }));
  };

  const guardar = async () => {
    setSaving(true);
    try {
      await servicioApi.put('/core/configuracion/', config);
      notif.success('Configuración guardada correctamente');
    } catch {
      notif.error('Error al guardar la configuración');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return (
    <div className="admin-loading">
      <div className="admin-spinner" />
      <span>Cargando configuración...</span>
    </div>
  );

  if (error) return (
    <div>
      <div className="admin-error-msg">{error}</div>
      <button className="btn-refresh" onClick={cargar}>
        <MultiPathIcon paths={[icons.refresh]} size={14} /> Reintentar
      </button>
    </div>
  );

  return (
    <div>
      <div className="config-grid">
        <div className="config-field">
          <label className="config-label">Porcentaje plataforma (%)</label>
          <input type="number" className="config-input" step="0.01" min="0" max="100"
            value={config?.porcentaje_plataforma ?? ''}
            onChange={e => handleChange('porcentaje_plataforma', e.target.value)} />
        </div>
        <div className="config-field">
          <label className="config-label">Puntos por resultado exacto</label>
          <input type="number" className="config-input" min="0"
            value={config?.puntos_exacto ?? ''}
            onChange={e => handleChange('puntos_exacto', parseInt(e.target.value, 10))} />
        </div>
        <div className="config-field">
          <label className="config-label">Puntos por ganador correcto</label>
          <input type="number" className="config-input" min="0"
            value={config?.puntos_ganador ?? ''}
            onChange={e => handleChange('puntos_ganador', parseInt(e.target.value, 10))} />
        </div>
        <div className="config-field">
          <label className="config-label">Máx. ligas por usuario</label>
          <input type="number" className="config-input" min="0" placeholder="Sin límite"
            value={config?.max_ligas_por_usuario ?? ''}
            onChange={e => handleChange('max_ligas_por_usuario', e.target.value || null)} />
        </div>
        <div className="config-field">
          <label className="config-label">Fecha inicio torneo</label>
          <input type="date" className="config-input"
            value={config?.fecha_inicio_torneo ?? ''}
            onChange={e => handleChange('fecha_inicio_torneo', e.target.value || null)} />
        </div>
        <div className="config-field">
          <label className="config-label">Fecha fin torneo</label>
          <input type="date" className="config-input"
            value={config?.fecha_fin_torneo ?? ''}
            onChange={e => handleChange('fecha_fin_torneo', e.target.value || null)} />
        </div>
        <div className="config-field">
          <label className="config-label">Registro abierto</label>
          <div className="config-toggle">
            <input type="checkbox" id="registro-abierto"
              checked={config?.permite_registro_abierto ?? true}
              onChange={e => handleChange('permite_registro_abierto', e.target.checked)} />
            <label htmlFor="registro-abierto" style={{ color: 'var(--text-secondary)', fontSize: 'var(--font-size-sm)' }}>
              Permitir que nuevos usuarios se registren
            </label>
          </div>
        </div>
      </div>
      <button className="btn-primary" onClick={guardar} disabled={saving}>
        {saving ? 'Guardando...' : 'Guardar Configuración'}
      </button>
    </div>
  );
};

// ── BITÁCORA ─────────────────────────────────────────────────────────────────

const Bitacora = () => {
  const [registros, setRegistros] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filtroUsuario, setFiltroUsuario] = useState('');
  const [filtroFecha, setFiltroFecha] = useState('');

  const cargar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = {};
      if (filtroUsuario) params.usuario_id = filtroUsuario;
      if (filtroFecha) params.fecha = filtroFecha;
      const res = await servicioApi.get('/core/bitacora/', { params });
      const data = res.data;
      setRegistros(Array.isArray(data) ? data : (data.results ?? []));
    } catch {
      setError('No se pudo cargar la bitácora.');
    } finally {
      setLoading(false);
    }
  }, [filtroUsuario, filtroFecha]);

  useEffect(() => {
    const t = setTimeout(() => cargar(), 350);
    return () => clearTimeout(t);
  }, [cargar]);

  return (
    <div>
      <div className="admin-filters">
        <input className="admin-search-input" type="text" placeholder="ID de usuario..."
          value={filtroUsuario} onChange={e => setFiltroUsuario(e.target.value)}
          autoComplete="off" style={{ maxWidth: 180 }} />
        <input className="admin-search-input" type="text" placeholder="Fecha (YYYY-MM-DD)..."
          value={filtroFecha} onChange={e => setFiltroFecha(e.target.value)}
          autoComplete="off" style={{ maxWidth: 200 }} />
        <button className="btn-refresh" onClick={cargar}>
          <MultiPathIcon paths={[icons.refresh]} size={14} /> Actualizar
        </button>
        {(filtroUsuario || filtroFecha) && (
          <button className="btn-refresh" onClick={() => { setFiltroUsuario(''); setFiltroFecha(''); }}>
            Limpiar filtros
          </button>
        )}
      </div>

      {error && <div className="admin-error-msg">{error}</div>}

      {loading ? (
        <div className="admin-loading"><div className="admin-spinner" /><span>Cargando bitácora...</span></div>
      ) : registros.length === 0 ? (
        <div className="admin-empty">
          <MultiPathIcon paths={[icons.bitacora]} size={48} />
          <p>No hay registros en la bitácora</p>
        </div>
      ) : (
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr>
                <th>Nro.</th>
                <th>Fecha</th>
                <th>Hora</th>
                <th>Usuario ID</th>
                <th>Detalle</th>
              </tr>
            </thead>
            <tbody>
              {registros.map((r, i) => (
                <tr key={r.log ?? i}>
                  <td style={{ color: 'var(--text-muted)' }}>{r.log}</td>
                  <td>{fmtDate(r.fecha)}</td>
                  <td style={{ color: 'var(--text-tertiary)' }}>{r.hora}</td>
                  <td>
                    <span className="badge badge-info">{r.fk_id_usuario}</span>
                  </td>
                  <td>{r.detalle_accion}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="admin-table-footer">{registros.length} registro(s)</div>
        </div>
      )}
    </div>
  );
};

// ── AUDIT LOG ────────────────────────────────────────────────────────────────

const POR_PAGINA = 15;

const PaginacionControles = ({ pagina, totalPaginas, onChange }) => {
  if (totalPaginas <= 1) return null;

  const rango = () => {
    const delta = 2;
    const inicio = Math.max(1, pagina - delta);
    const fin = Math.min(totalPaginas, pagina + delta);
    const paginas = [];
    if (inicio > 1) { paginas.push(1); if (inicio > 2) paginas.push('...'); }
    for (let i = inicio; i <= fin; i++) paginas.push(i);
    if (fin < totalPaginas) { if (fin < totalPaginas - 1) paginas.push('...'); paginas.push(totalPaginas); }
    return paginas;
  };

  return (
    <div className="paginacion">
      <button className="paginacion-btn" disabled={pagina === 1} onClick={() => onChange(pagina - 1)}>
        ‹ Anterior
      </button>
      <div className="paginacion-paginas">
        {rango().map((p, i) =>
          p === '...'
            ? <span key={`e-${i}`} className="paginacion-ellipsis">…</span>
            : <button key={p} className={`paginacion-num ${pagina === p ? 'activo' : ''}`} onClick={() => onChange(p)}>
                {p}
              </button>
        )}
      </div>
      <button className="paginacion-btn" disabled={pagina === totalPaginas} onClick={() => onChange(pagina + 1)}>
        Siguiente ›
      </button>
    </div>
  );
};

const AuditLog = () => {
  const [registros, setRegistros] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filtroTabla, setFiltroTabla] = useState('');
  const [filtroOp, setFiltroOp] = useState('');
  const [pagina, setPagina] = useState(1);
  const [totalRegistros, setTotalRegistros] = useState(0);

  const cargar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = {
        page: pagina,
        page_size: POR_PAGINA
      };
      if (filtroTabla) params.table_name = filtroTabla;
      if (filtroOp) params.operation = filtroOp;
      const res = await servicioApi.get('/core/audit-log/', { params });
      const data = res.data;
      //Debugear los 15 primeros registros
      //console.log('AuditLog response:', data.results.slice(0, 15));
      setRegistros(data.results ?? []);
      setTotalRegistros(data.count ?? 0);
    } catch {
      setError('No se pudo cargar el log de auditoría.');
    } finally {
      setLoading(false);
    }
  }, [filtroTabla, filtroOp, pagina]);

  useEffect(() => {
    cargar();
  }, [cargar]);

  const totalPaginas = Math.ceil(totalRegistros / POR_PAGINA);

  const handleFiltroChange = () => {
    setPagina(1);
  };

  const handlePaginaChange = (nuevaPagina) => {
    setPagina(nuevaPagina);
  };

  return (
    <div>
      <div className="admin-filters">
        <input className="admin-search-input" placeholder="Tabla (ej: liga, partido)..."
          value={filtroTabla} onChange={e => { setFiltroTabla(e.target.value); handleFiltroChange(); }}
          style={{ maxWidth: 220 }} />
        <select className="admin-select" value={filtroOp} onChange={e => { setFiltroOp(e.target.value); handleFiltroChange(); }}>
          <option value="">Todas las operaciones</option>
          <option value="INSERT">INSERT</option>
          <option value="UPDATE">UPDATE</option>
          <option value="DELETE">DELETE</option>
        </select>
        <button className="btn-refresh" onClick={cargar}>
          <MultiPathIcon paths={[icons.refresh]} size={14} /> Actualizar
        </button>
        {(filtroTabla || filtroOp) && (
          <button className="btn-refresh" onClick={() => { setFiltroTabla(''); setFiltroOp(''); handleFiltroChange(); }}>
            Limpiar filtros
          </button>
        )}
      </div>

      {error && <div className="admin-error-msg">{error}</div>}

      {loading ? (
        <div className="admin-loading"><div className="admin-spinner" /><span>Cargando audit log...</span></div>
      ) : registros.length === 0 ? (
        <div className="admin-empty">
          <MultiPathIcon paths={[icons.auditlog]} size={48} />
          <p>No hay registros en el audit log</p>
        </div>
      ) : (
        <>
          <div className="admin-table-wrapper">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Tabla</th>
                  <th>Operación</th>
                  <th>Registro ID</th>
                  <th>Fecha</th>
                  <th>Datos</th>
                </tr>
              </thead>
              <tbody>
                {registros.map((r, i) => (
                  <tr key={r.id ?? i}>
                    <td style={{ color: 'var(--text-muted)' }}>{r.id}</td>
                    <td><span className="badge badge-info">{r.table_name}</span></td>
                    <td>
                      <span className={`badge ${
                        r.operation === 'INSERT' ? 'badge-success' :
                        r.operation === 'DELETE' ? 'badge-danger' : 'badge-warning'
                      }`}>{r.operation}</span>
                    </td>
                    <td style={{ color: 'var(--text-tertiary)' }}>{r.record_id}</td>
                    <td style={{ color: 'var(--text-tertiary)', whiteSpace: 'nowrap' }}>
                      {fmtDatetime(r.changed_at)}
                    </td>
                    <td style={{ maxWidth: 300, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      <span title={JSON.stringify(r.new_data)}>
                        {r.new_data ? JSON.stringify(r.new_data).slice(0, 80) + '…' : '—'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="admin-table-footer">
              <span>
                Mostrando {registros.length} de {totalRegistros} registro(s)
              </span>
              <span>{POR_PAGINA} por página</span>
            </div>
          </div>

          <PaginacionControles pagina={pagina} totalPaginas={totalPaginas} onChange={handlePaginaChange} />
        </>
      )}
    </div>
  );
};

// ── MAIN PAGE ─────────────────────────────────────────────────────────────────

const SECCIONES = [
  { id: 'dashboard', label: 'Dashboard',    iconPath: icons.dashboard },
  { id: 'usuarios',  label: 'Usuarios',     iconPath: icons.users },
  { id: 'config',    label: 'Configuración',iconPath: icons.config },
  { id: 'bitacora',  label: 'Bitácora',     iconPath: icons.bitacora },
  { id: 'auditlog',  label: 'Audit Log',    iconPath: icons.auditlog },
];

const TITULOS = {
  dashboard: 'Dashboard del Sistema',
  usuarios:  'Gestión de Usuarios',
  config:    'Configuración del Torneo',
  bitacora:  'Bitácora de Actividad',
  auditlog:  'Log de Auditoría',
};

const AdminPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const notif = useNotificaciones();
  const [seccion, setSeccion] = useState('dashboard');

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const renderSeccion = () => {
    switch (seccion) {
      case 'dashboard': return <Dashboard />;
      case 'usuarios':  return <GestionUsuarios notif={notif} />;
      case 'config':    return <ConfiguracionTorneo notif={notif} />;
      case 'bitacora':  return <Bitacora />;
      case 'auditlog':  return <AuditLog />;
      default:          return null;
    }
  };

  return (
    <div className="admin-container">
      <div className="admin-background">
        <AdminTopBar user={user} onBack={() => navigate('/home')} onLogout={handleLogout} />

        <div className="admin-layout">
          <nav className="admin-sidebar">
            {SECCIONES.map(s => (
              <button key={s.id}
                className={`admin-nav-item ${seccion === s.id ? 'active' : ''}`}
                onClick={() => setSeccion(s.id)}>
                <MultiPathIcon paths={[s.iconPath]} size={18} />
                {s.label}
              </button>
            ))}
          </nav>

          <main className="admin-content">
            <div className="admin-panel">
              <div className="admin-panel-header">
                <div className="admin-panel-title">
                  <MultiPathIcon
                    paths={[SECCIONES.find(s => s.id === seccion)?.iconPath]}
                    size={24} />
                  <h2>{TITULOS[seccion]}</h2>
                </div>
              </div>
              {renderSeccion()}
            </div>
          </main>
        </div>
      </div>

      <NotificacionesContainer
        notificaciones={notif.notificaciones}
        onClose={notif.cerrarNotificacion}
      />
    </div>
  );
};

export default AdminPage;
