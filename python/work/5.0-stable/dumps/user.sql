--
-- PostgreSQL database dump
--

-- Dumped from database version 9.0.3
-- Dumped by pg_dump version 9.0.3
-- Started on 2012-02-20 14:01:19 MSK

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 1833 (class 1259 OID 16480)
-- Dependencies: 5
-- Name: auth_user; Type: TABLE; Schema: public; Owner: sa; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    password character varying(128) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO sa;

--
-- TOC entry 1832 (class 1259 OID 16478)
-- Dependencies: 1833 5
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: sa
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO sa;

--
-- TOC entry 2297 (class 0 OID 0)
-- Dependencies: 1832
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sa
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- TOC entry 2298 (class 0 OID 0)
-- Dependencies: 1832
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sa
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, true);


--
-- TOC entry 2289 (class 2604 OID 16483)
-- Dependencies: 1832 1833 1833
-- Name: id; Type: DEFAULT; Schema: public; Owner: sa
--

ALTER TABLE auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- TOC entry 2294 (class 0 OID 16480)
-- Dependencies: 1833
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: sa
--

COPY auth_user (id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined) FROM stdin;
1	admin			suport@smilart.com	sha1$c9a32$aefcf04421aa53b31e701c4561d0f1700bea7b1c	t	t	t	2012-02-20 09:53:45.299044+03	2012-02-14 14:47:08.003542+03
\.


--
-- TOC entry 2291 (class 2606 OID 16485)
-- Dependencies: 1833 1833
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: sa; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- TOC entry 2293 (class 2606 OID 16487)
-- Dependencies: 1833 1833
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: sa; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


-- Completed on 2012-02-20 14:01:19 MSK

--
-- PostgreSQL database dump complete
--

