CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    mail VARCHAR(150) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL
)
-- ########################################################################--

CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    place VARCHAR(100) NOT NULL,
    issue TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'open',
    assigned VARCHAR(100)
);
-- ########################################################################--