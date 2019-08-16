

CREATE TABLE IF NOT EXISTS users (
    username character varying(50) PRIMARY KEY NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    ek_number character varying(6) NOT NULL,
    email character varying(50) NOT NULL,
    phone_number character varying(10) NOT NULL,
    profile character varying(10) NULL,
    password character varying(100) NOT NULL,
    position character varying(50) NULL,
    user_level numeric (1) DEFAULT 1,
    active numeric (1) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS blacklist (
    tokens character varying(200) NOT NULL,
    timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS projects (
    _id numeric (5) PRIMARY KEY NOT NULL,
    name CHARACTER varying(50) NOT NULL,
    default_owner CHARACTER varying(50) NOT NULL,
    description CHARACTER varying(500) NOT NULL,
    start_date DATE NOT NULL,
    owner CHARACTER varying(50) NULL,
    created_by CHARACTER varying(50) NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

