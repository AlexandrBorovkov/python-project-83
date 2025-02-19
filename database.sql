CREATE TABLE IF NOT EXISTS urls (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE
);


CREATE TABLE IF NOT EXISTS url_checks (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id BIGINT REFERENCES urls(id) NOT NULL,
    status_code INT,
    h1 VARCHAR(200),
    title VARCHAR(200),
    description VARCHAR(500),
    created_at DATE DEFAULT CURRENT_DATE
);