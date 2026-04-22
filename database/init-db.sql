--
-- PostgreSQL database dump
--

\restrict 7Hpn2sIihswh4XAuPxR1fe5o2a6TWNDyPVROSlnxS9ahweTnrEyZg9kr8GUqJYz

-- Dumped from database version 16.13 (Debian 16.13-1.pgdg13+1)
-- Dumped by pg_dump version 16.13 (Debian 16.13-1.pgdg13+1)
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;


SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bitacora; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bitacora (
    log integer NOT NULL,
    hora time without time zone DEFAULT CURRENT_TIME,
    fecha date DEFAULT CURRENT_DATE,
    detalle_accion text,
    fk_id_usuario integer
);


ALTER TABLE public.bitacora OWNER TO postgres;

--
-- Name: bitacora_log_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bitacora_log_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bitacora_log_seq OWNER TO postgres;

--
-- Name: bitacora_log_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bitacora_log_seq OWNED BY public.bitacora.log;


--
-- Name: equipoliga; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.equipoliga (
    fk_id_liga integer NOT NULL,
    fk_id_seleccion integer NOT NULL
);


ALTER TABLE public.equipoliga OWNER TO postgres;

--
-- Name: fase_grupo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fase_grupo (
    id_fase integer NOT NULL,
    nombre_fase character varying(50) NOT NULL
);


ALTER TABLE public.fase_grupo OWNER TO postgres;

--
-- Name: fase_grupo_id_fase_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fase_grupo_id_fase_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.fase_grupo_id_fase_seq OWNER TO postgres;

--
-- Name: fase_grupo_id_fase_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fase_grupo_id_fase_seq OWNED BY public.fase_grupo.id_fase;


--
-- Name: gol; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gol (
    id_gol integer NOT NULL,
    fk_id_partido integer,
    fk_id_jugador integer,
    minuto_marcado integer,
    CONSTRAINT gol_minuto_marcado_check CHECK ((minuto_marcado > 0))
);


ALTER TABLE public.gol OWNER TO postgres;

--
-- Name: gol_id_gol_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.gol_id_gol_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gol_id_gol_seq OWNER TO postgres;

--
-- Name: gol_id_gol_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.gol_id_gol_seq OWNED BY public.gol.id_gol;




--
-- Name: historial_ganador; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.historial_ganador (
    id_pago integer NOT NULL,
    fk_id_usuario integer,
    fk_id_liga integer,
    monto_pagado numeric(10,2),
    fecha_premio timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status boolean DEFAULT true
);


ALTER TABLE public.historial_ganador OWNER TO postgres;

--
-- Name: historial_ganador_id_pago_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.historial_ganador_id_pago_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.historial_ganador_id_pago_seq OWNER TO postgres;

--
-- Name: historial_ganador_id_pago_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.historial_ganador_id_pago_seq OWNED BY public.historial_ganador.id_pago;


--
-- Name: jugador; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jugador (
    id_jugador integer NOT NULL,
    primer_nombre character varying(50),
    segundo_nombre character varying(50),
    primer_apellido character varying(50),
    segundo_apellido character varying(50),
    fecha_nacimiento date,
    dorsal integer,
    posicion character varying(50),
    fk_id_seleccion integer,
    status boolean DEFAULT true
);


ALTER TABLE public.jugador OWNER TO postgres;

--
-- Name: jugador_id_jugador_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.jugador_id_jugador_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.jugador_id_jugador_seq OWNER TO postgres;

--
-- Name: jugador_id_jugador_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.jugador_id_jugador_seq OWNED BY public.jugador.id_jugador;


--
-- Name: liga; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.liga (
    id_liga integer NOT NULL,
    nombre_liga character varying(100) NOT NULL,
    fk_administrador integer,
    monto_total_recaudado numeric(10,2) DEFAULT 0,
    estado character varying(50),
    tipo_liga character varying(50) DEFAULT 'Diversion'::character varying,
    status boolean DEFAULT true
);


ALTER TABLE public.liga OWNER TO postgres;

--
-- Name: liga_id_liga_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.liga_id_liga_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.liga_id_liga_seq OWNER TO postgres;

--
-- Name: liga_id_liga_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.liga_id_liga_seq OWNED BY public.liga.id_liga;


--
-- Name: invitacion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invitacion (
    id_invitacion integer NOT NULL,
    fk_id_liga integer NOT NULL,
    fk_id_usuario_invitado integer NOT NULL,
    fk_id_usuario_administrador integer NOT NULL,
    fecha_invitacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    estado_invitacion character varying(50) DEFAULT 'Pendiente'::character varying,
    mensaje_invitacion text
);


ALTER TABLE public.invitacion OWNER TO postgres;

--
-- Name: invitacion_id_invitacion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.invitacion_id_invitacion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.invitacion_id_invitacion_seq OWNER TO postgres;

--
-- Name: invitacion_id_invitacion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.invitacion_id_invitacion_seq OWNED BY public.invitacion.id_invitacion;


--
-- Name: participante_liga; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participante_liga (
    id_participante integer NOT NULL,
    fk_id_liga integer NOT NULL,
    fk_id_usuario integer NOT NULL,
    fecha_union timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    estado_participacion character varying(50) DEFAULT 'Activo'::character varying,
    status boolean DEFAULT true
);


ALTER TABLE public.participante_liga OWNER TO postgres;

--
-- Name: participante_liga_id_participante_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.participante_liga_id_participante_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.participante_liga_id_participante_seq OWNER TO postgres;

--
-- Name: participante_liga_id_participante_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.participante_liga_id_participante_seq OWNED BY public.participante_liga.id_participante;


--
-- Name: partido; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.partido (
    id_partido integer NOT NULL,
    horario timestamp without time zone,
    equipo_local integer,
    equipo_visitante integer,
    fk_sede integer,
    fk_id_fase integer,
    gol_local integer DEFAULT 0,
    gol_visitante integer DEFAULT 0,
    ganador_penales integer,
    tipo_partido character varying(50) DEFAULT 'Regular'::character varying,
    resultado character varying(50),
    CONSTRAINT partido_gol_local_check CHECK ((gol_local >= 0)),
    CONSTRAINT partido_gol_visitante_check CHECK ((gol_visitante >= 0))
);


ALTER TABLE public.partido OWNER TO postgres;

--
-- Name: partido_id_partido_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.partido_id_partido_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.partido_id_partido_seq OWNER TO postgres;

--
-- Name: partido_id_partido_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.partido_id_partido_seq OWNED BY public.partido.id_partido;


--
-- Name: partido_liga; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.partido_liga (
    fk_id_liga integer NOT NULL,
    fk_id_partido integer NOT NULL
);


ALTER TABLE public.partido_liga OWNER TO postgres;


--
-- Name: posiciones_torneo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.posiciones_torneo (
    id_posicion integer NOT NULL,
    fk_id_fase integer,
    fk_id_seleccion integer,
    pj integer DEFAULT 0,
    pg integer DEFAULT 0,
    pe integer DEFAULT 0,
    pp integer DEFAULT 0,
    gf integer DEFAULT 0,
    gc integer DEFAULT 0,
    puntos integer DEFAULT 0
);


ALTER TABLE public.posiciones_torneo OWNER TO postgres;

--
-- Name: posiciones_torneo_id_posicion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.posiciones_torneo_id_posicion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.posiciones_torneo_id_posicion_seq OWNER TO postgres;

--
-- Name: posiciones_torneo_id_posicion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.posiciones_torneo_id_posicion_seq OWNED BY public.posiciones_torneo.id_posicion;


--
-- Name: premio; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.premio (
    id_premio integer NOT NULL,
    fk_id_liga integer,
    posicion integer,
    porcentaje_premio numeric(5,2)
);


ALTER TABLE public.premio OWNER TO postgres;

--
-- Name: premio_id_premio_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.premio_id_premio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.premio_id_premio_seq OWNER TO postgres;

--
-- Name: premio_id_premio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.premio_id_premio_seq OWNED BY public.premio.id_premio;


--
-- Name: pronostico; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pronostico (
    id_pronostico integer NOT NULL,
    fk_id_usuario integer,
    fk_id_partido integer,
    fk_id_liga integer,
    gol_local integer,
    gol_visitante integer,
    CONSTRAINT pronostico_gol_local_check CHECK ((gol_local >= 0)),
    CONSTRAINT pronostico_gol_visitante_check CHECK ((gol_visitante >= 0)),
    status boolean DEFAULT true
);


ALTER TABLE public.pronostico OWNER TO postgres;

--
-- Name: pronostico_id_pronostico_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pronostico_id_pronostico_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pronostico_id_pronostico_seq OWNER TO postgres;

--
-- Name: pronostico_id_pronostico_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pronostico_id_pronostico_seq OWNED BY public.pronostico.id_pronostico;


--
-- Name: ranking; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ranking (
    id_registro integer NOT NULL,
    puntos integer DEFAULT 0,
    fk_id_usuario integer,
    fk_id_liga integer,
    pj integer DEFAULT 0,
    fecha_actualizacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status boolean DEFAULT true
);


ALTER TABLE public.ranking OWNER TO postgres;

--
-- Name: ranking_id_registro_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ranking_id_registro_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ranking_id_registro_seq OWNER TO postgres;

--
-- Name: ranking_id_registro_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ranking_id_registro_seq OWNED BY public.ranking.id_registro;


--
-- Name: rol_usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rol_usuario (
    id_rol integer NOT NULL,
    descripcion character varying(50) NOT NULL
);


ALTER TABLE public.rol_usuario OWNER TO postgres;

--
-- Name: rol_usuario_id_rol_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rol_usuario_id_rol_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rol_usuario_id_rol_seq OWNER TO postgres;

--
-- Name: rol_usuario_id_rol_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rol_usuario_id_rol_seq OWNED BY public.rol_usuario.id_rol;


--
-- Name: sede; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sede (
    id_sede integer NOT NULL,
    ciudad character varying(100),
    estadio character varying(100)
);


ALTER TABLE public.sede OWNER TO postgres;

--
-- Name: sede_id_sede_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sede_id_sede_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sede_id_sede_seq OWNER TO postgres;

--
-- Name: sede_id_sede_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sede_id_sede_seq OWNED BY public.sede.id_sede;


--
-- Name: seleccion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seleccion (
    id_seleccion integer NOT NULL,
    pais character varying(100) NOT NULL,
    bandera character varying(255),
    fk_id_fase_inicial integer,
    status boolean DEFAULT true
);


ALTER TABLE public.seleccion OWNER TO postgres;

--
-- Name: seleccion_id_seleccion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seleccion_id_seleccion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.seleccion_id_seleccion_seq OWNER TO postgres;

--
-- Name: seleccion_id_seleccion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.seleccion_id_seleccion_seq OWNED BY public.seleccion.id_seleccion;


--
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    id_usuario integer NOT NULL,
    primer_nombre character varying(50),
    segundo_nombre character varying(50),
    primer_apellido character varying(50),
    segundo_apellido character varying(50),
    fecha_nacimiento date,
    email character varying(100) NOT NULL,
    telefono integer,
    contrasena character varying(255) NOT NULL,
    fk_rol integer,
    status boolean DEFAULT true
);



ALTER TABLE public.usuario OWNER TO postgres;

--
-- Name: usuario_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuario_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuario_id_usuario_seq OWNER TO postgres;

--
-- Name: usuario_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuario_id_usuario_seq OWNED BY public.usuario.id_usuario;


--
-- Name: bitacora log; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bitacora ALTER COLUMN log SET DEFAULT nextval('public.bitacora_log_seq'::regclass);


--
-- Name: fase_grupo id_fase; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fase_grupo ALTER COLUMN id_fase SET DEFAULT nextval('public.fase_grupo_id_fase_seq'::regclass);


--
-- Name: gol id_gol; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gol ALTER COLUMN id_gol SET DEFAULT nextval('public.gol_id_gol_seq'::regclass);




--
-- Name: historial_ganador id_pago; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.historial_ganador ALTER COLUMN id_pago SET DEFAULT nextval('public.historial_ganador_id_pago_seq'::regclass);


--
-- Name: jugador id_jugador; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jugador ALTER COLUMN id_jugador SET DEFAULT nextval('public.jugador_id_jugador_seq'::regclass);


--
-- Name: liga id_liga; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.liga ALTER COLUMN id_liga SET DEFAULT nextval('public.liga_id_liga_seq'::regclass);


--
-- Name: invitacion id_invitacion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invitacion ALTER COLUMN id_invitacion SET DEFAULT nextval('public.invitacion_id_invitacion_seq'::regclass);


--
-- Name: participante_liga id_participante; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participante_liga ALTER COLUMN id_participante SET DEFAULT nextval('public.participante_liga_id_participante_seq'::regclass);


--
-- Name: partido id_partido; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.partido ALTER COLUMN id_partido SET DEFAULT nextval('public.partido_id_partido_seq'::regclass);


--
-- Name: posiciones_torneo id_posicion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posiciones_torneo ALTER COLUMN id_posicion SET DEFAULT nextval('public.posiciones_torneo_id_posicion_seq'::regclass);


--
-- Name: premio id_premio; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.premio ALTER COLUMN id_premio SET DEFAULT nextval('public.premio_id_premio_seq'::regclass);


--
-- Name: pronostico id_pronostico; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pronostico ALTER COLUMN id_pronostico SET DEFAULT nextval('public.pronostico_id_pronostico_seq'::regclass);


--
-- Name: ranking id_registro; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ranking ALTER COLUMN id_registro SET DEFAULT nextval('public.ranking_id_registro_seq'::regclass);


--
-- Name: rol_usuario id_rol; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rol_usuario ALTER COLUMN id_rol SET DEFAULT nextval('public.rol_usuario_id_rol_seq'::regclass);


--
-- Name: sede id_sede; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sede ALTER COLUMN id_sede SET DEFAULT nextval('public.sede_id_sede_seq'::regclass);


--
-- Name: seleccion id_seleccion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seleccion ALTER COLUMN id_seleccion SET DEFAULT nextval('public.seleccion_id_seleccion_seq'::regclass);


--
-- Name: usuario id_usuario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuario_id_usuario_seq'::regclass);


--
-- Data for Name: bitacora; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bitacora (log, hora, fecha, detalle_accion, fk_id_usuario) FROM stdin;
\.


--
-- Data for Name: equipoliga; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.equipoliga (fk_id_liga, fk_id_seleccion) FROM stdin;
\.


--
-- Data for Name: fase_grupo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fase_grupo (id_fase, nombre_fase) FROM stdin;
\.


--
-- Data for Name: gol; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gol (id_gol, fk_id_partido, fk_id_jugador, minuto_marcado) FROM stdin;
\.




--
-- Data for Name: historial_ganador; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.historial_ganador (id_pago, fk_id_usuario, fk_id_liga, monto_pagado, fecha_premio) FROM stdin;
\.


--
-- Data for Name: jugador; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.jugador (id_jugador, primer_nombre, primer_apellido, dorsal, posicion, fk_id_seleccion) FROM stdin;
\.


--
-- Data for Name: liga; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.liga (id_liga, nombre_liga, fk_administrador, monto_total_recaudado, estado, tipo_liga) FROM stdin;
\.


--
-- Data for Name: invitacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invitacion (id_invitacion, fk_id_liga, fk_id_usuario_invitado, fk_id_usuario_administrador, fecha_invitacion, estado_invitacion, mensaje_invitacion) FROM stdin;
\.


--
-- Data for Name: participante_liga; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.participante_liga (id_participante, fk_id_liga, fk_id_usuario, fecha_union, estado_participacion) FROM stdin;
\.


--
-- Data for Name: partido; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.partido (id_partido, horario, equipo_local, equipo_visitante, fk_sede, fk_id_fase, gol_local, gol_visitante, ganador_penales, tipo_partido, resultado) FROM stdin;
\.


--
-- Data for Name: posiciones_torneo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.posiciones_torneo (id_posicion, fk_id_fase, fk_id_seleccion, pj, pg, pe, pp, gf, gc, puntos) FROM stdin;
\.


--
-- Data for Name: premio; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.premio (id_premio, fk_id_liga, posicion, porcentaje_premio) FROM stdin;
\.


--
-- Data for Name: pronostico; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pronostico (id_pronostico, fk_id_usuario, fk_id_partido, fk_id_liga, gol_local, gol_visitante) FROM stdin;
\.


--
-- Data for Name: ranking; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ranking (id_registro, puntos, fk_id_usuario, fk_id_liga, pj, fecha_actualizacion) FROM stdin;
\.


--
-- Data for Name: rol_usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rol_usuario (id_rol, descripcion) FROM stdin;
\.


--
-- Data for Name: sede; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sede (id_sede, ciudad, estadio) FROM stdin;
\.


--
-- Data for Name: seleccion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.seleccion (id_seleccion, pais, bandera, fk_id_fase_inicial) FROM stdin;
\.


--
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario (id_usuario, primer_nombre, primer_apellido, email, telefono, contrasena, fk_rol) FROM stdin;
\.


--
-- Name: bitacora_log_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bitacora_log_seq', 1, false);


--
-- Name: fase_grupo_id_fase_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fase_grupo_id_fase_seq', 1, false);


--
-- Name: gol_id_gol_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.gol_id_gol_seq', 1, false);




--
-- Name: historial_ganador_id_pago_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.historial_ganador_id_pago_seq', 1, false);


--
-- Name: jugador_id_jugador_seq; Type: SEQUENCE SET; Schema: public: Owner: postgres
--

SELECT pg_catalog.setval('public.jugador_id_jugador_seq', 1, false);


--
-- Name: liga_id_liga_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.liga_id_liga_seq', 1, false);


--
-- Name: invitacion_id_invitacion_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.invitacion_id_invitacion_seq', 1, false);


--
-- Name: participante_liga_id_participante_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.participante_liga_id_participante_seq', 1, false);


--
-- Name: partido_id_partido_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.partido_id_partido_seq', 1, false);


--
-- Name: posiciones_torneo_id_posicion_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.posiciones_torneo_id_posicion_seq', 1, false);


--
-- Name: premio_id_premio_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.premio_id_premio_seq', 1, false);


--
-- Name: pronostico_id_pronostico_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pronostico_id_pronostico_seq', 1, false);


--
-- Name: ranking_id_registro_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ranking_id_registro_seq', 1, false);


--
-- Name: rol_usuario_id_rol_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rol_usuario_id_rol_seq', 1, false);


--
-- Name: sede_id_sede_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sede_id_sede_seq', 1, false);


--
-- Name: seleccion_id_seleccion_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.seleccion_id_seleccion_seq', 1, false);


--
-- Name: usuario_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_id_usuario_seq', 1, false);


--
-- Name: bitacora bitacora_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bitacora
    ADD CONSTRAINT bitacora_pkey PRIMARY KEY (log);


--
-- Name: equipoliga equipoliga_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipoliga
    ADD CONSTRAINT equipoliga_pkey PRIMARY KEY (fk_id_liga, fk_id_seleccion);


--
-- Name: partido_liga partido_liga_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.partido_liga
    ADD CONSTRAINT partido_liga_pkey PRIMARY KEY (fk_id_liga, fk_id_partido);


--
-- Name: fase_grupo fase_grupo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fase_grupo
    ADD CONSTRAINT fase_grupo_pkey PRIMARY KEY (id_fase);


--
-- Name: gol gol_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gol
    ADD CONSTRAINT gol_pkey PRIMARY KEY (id_gol);




--
-- Name: historial_ganador historial_ganador_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.historial_ganador
    ADD CONSTRAINT historial_ganador_pkey PRIMARY KEY (id_pago);


--
-- Name: jugador jugador_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jugador
    ADD CONSTRAINT jugador_pkey PRIMARY KEY (id_jugador);


--
-- Name: liga liga_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.liga
    ADD CONSTRAINT liga_pkey PRIMARY KEY (id_liga);


--
-- Name: invitacion invitacion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invitacion
    ADD CONSTRAINT invitacion_pkey PRIMARY KEY (id_invitacion);


--
-- Name: participante_liga participante_liga_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participante_liga
    ADD CONSTRAINT participante_liga_pkey PRIMARY KEY (id_participante);


--
-- Name: partido partido_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.partido
    ADD CONSTRAINT partido_pkey PRIMARY KEY (id_partido);


--
-- Name: posiciones_torneo posiciones_torneo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posiciones_torneo
    ADD CONSTRAINT posiciones_torneo_pkey PRIMARY KEY (id_posicion);


--
-- Name: premio premio_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.premio
    ADD CONSTRAINT premio_pkey PRIMARY KEY (id_premio);


--
-- Name: pronostico pronostico_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pronostico
    ADD CONSTRAINT pronostico_pkey PRIMARY KEY (id_pronostico);


--
-- Name: ranking ranking_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ranking
    ADD CONSTRAINT ranking_pkey PRIMARY KEY (id_registro);


--
-- Name: rol_usuario rol_usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rol_usuario
    ADD CONSTRAINT rol_usuario_pkey PRIMARY KEY (id_rol);


--
-- Name: sede sede_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sede
    ADD CONSTRAINT sede_pkey PRIMARY KEY (id_sede);


--
-- Name: seleccion seleccion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seleccion
    ADD CONSTRAINT seleccion_pkey PRIMARY KEY (id_seleccion);


--
-- Name: ranking uq_ranking_usuario_liga; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ranking
    ADD CONSTRAINT uq_ranking_usuario_liga UNIQUE (fk_id_usuario, fk_id_liga);


--
-- Name: participante_liga uq_participante_liga_usuario_liga; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participante_liga
    ADD CONSTRAINT uq_participante_liga_usuario_liga UNIQUE (fk_id_usuario, fk_id_liga);


--
-- Name: posiciones_torneo uq_seleccion_fase; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posiciones_torneo
    ADD CONSTRAINT uq_seleccion_fase UNIQUE (fk_id_seleccion, fk_id_fase);


--
-- Name: pronostico uq_usuario_partido_liga; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pronostico
    ADD CONSTRAINT uq_usuario_partido_liga UNIQUE (fk_id_usuario, fk_id_partido, fk_id_liga);


--
-- Name: usuario usuario_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_email_key UNIQUE (email);


--
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario);


--
-- Name: bitacora bitacora_fk_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bitacora
    ADD CONSTRAINT bitacora_fk_id_usuario_fkey FOREIGN KEY (fk_id_usuario) REFERENCES public.usuario(id_usuario);


--
-- Name: equipoliga equipoliga_fk_id_liga_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipoliga
    ADD CONSTRAINT equipoliga_fk_id_liga_fkey FOREIGN KEY (fk_id_liga) REFERENCES public.liga(id_liga) ON DELETE CASCADE;


--
-- Name: equipoliga equipoliga_fk_id_seleccion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipoliga
    ADD CONSTRAINT equipoliga_fk_id_seleccion_fkey FOREIGN KEY (fk_id_seleccion) REFERENCES public.seleccion(id_seleccion) ON DELETE CASCADE;


--
-- Name: partido_liga partido_liga_fk_id_liga_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.partido_liga
    ADD CONSTRAINT partido_liga_fk_id_liga_fkey FOREIGN KEY (fk_id_liga) REFERENCES public.liga(id_liga) ON DELETE CASCADE;


--
-- Name: partido_liga partido_liga_fk_id_partido_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.partido_liga
    ADD CONSTRAINT partido_liga_fk_id_partido_fkey FOREIGN KEY (fk_id_partido) REFERENCES public.partido(id_partido) ON DELETE CASCADE;


--
-- Name: gol gol_fk_id_jugador_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gol
    ADD CONSTRAINT gol_fk_id_jugador_fkey FOREIGN KEY (fk_id_jugador) REFERENCES public.jugador(id_jugador);


--
-- Name: gol gol_fk_id_partido_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gol
    ADD CONSTRAINT gol_fk_id_partido_fkey FOREIGN KEY (fk_id_partido) REFERENCES public.partido(id_partido) ON DELETE CASCADE;


--
-- Name: historial_ganador historial_ganador_fk_id_liga_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.historial_ganador
    ADD CONSTRAINT historial_ganador_fk_id_liga_fkey FOREIGN KEY (fk_id_liga) REFERENCES public.liga(id_liga);


--
-- Name: historial_ganador historial_ganador_fk_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.historial_ganador
    ADD CONSTRAINT historial_ganador_fk_id_usuario_fkey FOREIGN KEY (fk_id_usuario) REFERENCES public.usuario(id_usuario);


--
-- Name: jugador jugador_fk_id_seleccion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jugador
    ADD CONSTRAINT jugador_fk_id_seleccion_fkey FOREIGN KEY (fk_id_seleccion) REFERENCES public.seleccion(id_seleccion) ON DELETE CASCADE;


--
-- Name: liga liga_fk_administrador_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.liga
    ADD CONSTRAINT liga_fk_administrador_fkey FOREIGN KEY (fk_administrador) REFERENCES public.usuario(id_usuario);


--
-- Name: invitacion invitacion_fk_id_liga_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invitacion
    ADD CONSTRAINT invitacion_fk_id_liga_fkey FOREIGN KEY (fk_id_liga) REFERENCES public.liga(id_liga) ON DELETE CASCADE;


--
-- Name: invitacion invitacion_fk_id_usuario_administrador_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invitacion
    ADD CONSTRAINT invitacion_fk_id_usuario_administrador_fkey FOREIGN KEY (fk_id_usuario_administrador) REFERENCES public.usuario(id_usuario);


--
-- Name: invitacion invitacion_fk_id_usuario_invitado_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invitacion
    ADD CONSTRAINT invitacion_fk_id_usuario_invitado_fkey FOREIGN KEY (fk_id_usuario_invitado) REFERENCES public.usuario(id_usuario);


--
-- Agregar columna email_invitado para invitaciones por email
--
ALTER TABLE public.invitacion ADD COLUMN email_invitado character varying(100);


--
-- Name: participante_liga participante_liga_fk_id_liga_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participante_liga
    ADD CONSTRAINT participante_liga_fk_id_liga_fkey FOREIGN KEY (fk_id_liga) REFERENCES public.liga(id_liga) ON DELETE CASCADE;


--
-- Name: participante_liga participante_liga_fk_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participante_liga
    ADD CONSTRAINT participante_liga_fk_id_usuario_fkey FOREIGN KEY (fk_id_usuario) REFERENCES public.usuario(id_usuario);


--
-- Name: partido partido_equipo_local_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.partido
    ADD CONSTRAINT partido_equipo_local_fkey FOREIGN KEY (equipo_local) REFERENCES public.seleccion(id_seleccion);


--
-- Name: partido partido_equipo_visitante_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.partido
    ADD CONSTRAINT partido_equipo_visitante_fkey FOREIGN KEY (equipo_visitante) REFERENCES public.seleccion(id_seleccion);


--
-- Name: partido partido_fk_id_fase_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.partido
    ADD CONSTRAINT partido_fk_id_fase_fkey FOREIGN KEY (fk_id_fase) REFERENCES public.fase_grupo(id_fase);


--
-- Name: partido partido_fk_sede_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.partido
    ADD CONSTRAINT partido_fk_sede_fkey FOREIGN KEY (fk_sede) REFERENCES public.sede(id_sede);


--
-- Name: partido partido_ganador_penales_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.partido
    ADD CONSTRAINT partido_ganador_penales_fkey FOREIGN KEY (ganador_penales) REFERENCES public.seleccion(id_seleccion);


--
-- Name: posiciones_torneo posiciones_torneo_fk_id_fase_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posiciones_torneo
    ADD CONSTRAINT posiciones_torneo_fk_id_fase_fkey FOREIGN KEY (fk_id_fase) REFERENCES public.fase_grupo(id_fase);


--
-- Name: posiciones_torneo posiciones_torneo_fk_id_seleccion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posiciones_torneo
    ADD CONSTRAINT posiciones_torneo_fk_id_seleccion_fkey FOREIGN KEY (fk_id_seleccion) REFERENCES public.seleccion(id_seleccion);


--
-- Name: pronostico pronostico_fk_id_liga_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pronostico
    ADD CONSTRAINT pronostico_fk_id_liga_fkey FOREIGN KEY (fk_id_liga) REFERENCES public.liga(id_liga);


--
-- Name: pronostico pronostico_fk_id_partido_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pronostico
    ADD CONSTRAINT pronostico_fk_id_partido_fkey FOREIGN KEY (fk_id_partido) REFERENCES public.partido(id_partido);


--
-- Name: pronostico pronostico_fk_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pronostico
    ADD CONSTRAINT pronostico_fk_id_usuario_fkey FOREIGN KEY (fk_id_usuario) REFERENCES public.usuario(id_usuario);


--
-- Name: ranking ranking_fk_id_liga_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ranking
    ADD CONSTRAINT ranking_fk_id_liga_fkey FOREIGN KEY (fk_id_liga) REFERENCES public.liga(id_liga);


--
-- Name: ranking ranking_fk_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ranking
    ADD CONSTRAINT ranking_fk_id_usuario_fkey FOREIGN KEY (fk_id_usuario) REFERENCES public.usuario(id_usuario);


--
-- Name: seleccion seleccion_fk_id_fase_inicial_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seleccion
    ADD CONSTRAINT seleccion_fk_id_fase_inicial_fkey FOREIGN KEY (fk_id_fase_inicial) REFERENCES public.fase_grupo(id_fase);


--
-- Name: usuario usuario_fk_rol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_fk_rol_fkey FOREIGN KEY (fk_rol) REFERENCES public.rol_usuario(id_rol);

INSERT INTO rol_usuario (id_rol, descripcion) 
VALUES 
(1, 'Admin'), 
(2, 'User');

INSERT INTO public.usuario (
    id_usuario, 
    primer_nombre, 
    segundo_nombre, 
    primer_apellido, 
    segundo_apellido, 
    fecha_nacimiento, 
    email, 
    telefono, 
    contrasena,
    fk_rol,
    status
) VALUES (
    1,                      
    'Admin',                
    NULL,                   
    'Principal',             
    NULL,                   
    '1990-01-01',            
    'admin@mundial.com',    
    12345678,           
    'bcrypt_sha256$$2b$12$X0maiGq0O0lRxPsyuVAgEOIlhZ2FFbvSNtWHI0gpHuWUhM8vAv7UC',
    1,
    true                        
) ON CONFLICT (id_usuario) DO NOTHING;

-- Restart sequence to start from 2 (skip ID 1 for admin user)
SELECT setval('public.usuario_id_usuario_seq', 2, true);

-- ============ DATOS DE EJEMPLO PARA PRUEBAS ============

-- Fases del torneo
INSERT INTO fase_grupo (id_fase, nombre_fase) VALUES 
(1, 'Fase de Grupos'),
(2, 'Octavos de Final'),
(3, 'Cuartos de Final'),
(4, 'Semifinales'),
(5, 'Final'),
(6, 'Tercer Lugar')
ON CONFLICT (id_fase) DO NOTHING;
SELECT setval('public.fase_grupo_id_fase_seq', 7, true);

-- Sedes (estadios)
INSERT INTO sede (id_sede, ciudad, estadio) VALUES 
(1, 'Ciudad de Guatemala', 'Estadio Doroteo Guamuch Flores'),
(2, 'Quetzaltenango', 'Estadio Mario Camposeco'),
(3, 'Antigua Guatemala', 'Estadio Pensativo'),
(4, 'Escuintla', 'Estadio Ricardo Saprissa')
ON CONFLICT (id_sede) DO NOTHING;
SELECT setval('public.sede_id_sede_seq', 5, true);

-- Selecciones participantes
INSERT INTO seleccion (id_seleccion, pais, bandera, fk_id_fase_inicial) VALUES 
(1, 'Guatemala', 'https://flagcdn.com/gt.svg', 1),
(2, 'México', 'https://flagcdn.com/mx.svg', 1),
(3, 'Estados Unidos', 'https://flagcdn.com/us.svg', 1),
(4, 'Costa Rica', 'https://flagcdn.com/cr.svg', 1),
(5, 'Honduras', 'https://flagcdn.com/hn.svg', 1),
(6, 'El Salvador', 'https://flagcdn.com/sv.svg', 1),
(7, 'Panamá', 'https://flagcdn.com/pa.svg', 1),
(8, 'Canadá', 'https://flagcdn.com/ca.svg', 1),
(9, 'Argentina', 'https://flagcdn.com/ar.svg', 1),
(10, 'Brasil', 'https://flagcdn.com/br.svg', 1),
(11, 'Colombia', 'https://flagcdn.com/co.svg', 1),
(12, 'Uruguay', 'https://flagcdn.com/uy.svg', 1)
ON CONFLICT (id_seleccion) DO NOTHING;
SELECT setval('public.seleccion_id_seleccion_seq', 13, true);

-- Partidos de ejemplo (con fechas futuras para poder pronosticar)
-- Partidos de Fase de Grupos
INSERT INTO partido (id_partido, horario, equipo_local, equipo_visitante, fk_sede, fk_id_fase, gol_local, gol_visitante, tipo_partido, resultado) VALUES 
(1, '2026-06-15 15:00:00', 1, 2, 1, 1, 0, 0, 'Regular', 'Pendiente'),
(2, '2026-06-15 18:00:00', 3, 4, 1, 1, 0, 0, 'Regular', 'Pendiente'),
(3, '2026-06-16 15:00:00', 5, 6, 2, 1, 0, 0, 'Regular', 'Pendiente'),
(4, '2026-06-16 18:00:00', 7, 8, 2, 1, 0, 0, 'Regular', 'Pendiente'),
(5, '2026-06-17 15:00:00', 9, 10, 3, 1, 0, 0, 'Regular', 'Pendiente'),
(6, '2026-06-17 18:00:00', 11, 12, 3, 1, 0, 0, 'Regular', 'Pendiente'),
(7, '2026-06-18 15:00:00', 1, 3, 4, 1, 0, 0, 'Regular', 'Pendiente'),
(8, '2026-06-18 18:00:00', 2, 4, 4, 1, 0, 0, 'Regular', 'Pendiente')
ON CONFLICT (id_partido) DO NOTHING;
SELECT setval('public.partido_id_partido_seq', 9, true);

--
-- PostgreSQL database dump complete
--

--
-- Name: sesion_usuario; Type: TABLE; Schema: public; Owner: postgres
-- Tabla para registrar inicios de sesion y estado activo en tiempo real
--

CREATE TABLE public.sesion_usuario (
    id_sesion integer NOT NULL,
    fk_id_usuario integer NOT NULL,
    token_sesion character varying(255) NOT NULL,
    fecha_inicio timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_ultima_actividad timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_cierre timestamp without time zone,
    estado_sesion character varying(20) DEFAULT 'Activa'::character varying NOT NULL,
    ip_address character varying(45),
    user_agent text,
    dispositivo character varying(100)
);


ALTER TABLE public.sesion_usuario OWNER TO postgres;


--
-- Name: sesion_usuario_id_sesion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sesion_usuario_id_sesion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sesion_usuario_id_sesion_seq OWNER TO postgres;


--
-- Name: sesion_usuario_id_sesion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sesion_usuario_id_sesion_seq OWNED BY public.sesion_usuario.id_sesion;


--
-- Name: sesion_usuario_id_sesion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion_usuario ALTER COLUMN id_sesion SET DEFAULT nextval('public.sesion_usuario_id_sesion_seq'::regclass);


--
-- Name: sesion_usuario sesion_usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion_usuario
    ADD CONSTRAINT sesion_usuario_pkey PRIMARY KEY (id_sesion);


--
-- Name: sesion_usuario sesion_usuario_fk_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion_usuario
    ADD CONSTRAINT sesion_usuario_fk_id_usuario_fkey FOREIGN KEY (fk_id_usuario) REFERENCES public.usuario(id_usuario) ON DELETE CASCADE;


--
-- Name: sesion_usuario sesion_usuario_token_sesion_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion_usuario
    ADD CONSTRAINT sesion_usuario_token_sesion_key UNIQUE (token_sesion);


--
-- Name: sesion_usuario_id_sesion_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sesion_usuario_id_sesion_seq', 1, false);


\unrestrict 7Hpn2sIihswh4XAuPxR1fe5o2a6TWNDyPVROSlnxS9ahweTnrEyZg9kr8GUqJYz
