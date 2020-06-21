CREATE TABLE services(
    service_id SERIAL PRIMARY KEY,
    service_name TEXT UNIQUE,
    created_on TIMESTAMP DEFAULT NOW()
);

CREATE TABLE start_urls(
    start_url_id SERIAL PRIMARY KEY,
    service_id INTEGER REFERENCES services(service_id),
    start_url_name TEXT UNIQUE,
    created_on TIMESTAMP DEFAULT NOW()
);

CREATE TABLE articles(
    article_id SERIAL PRIMARY KEY,
    service_id INTEGER REFERENCES services(service_id),
    article_url TEXT UNIQUE,
    created_on TIMESTAMP DEFAULT NOW()
);

CREATE TABLE article_tags(
    id SERIAL PRIMARY KEY,
    article_id INTEGER REFERENCES articles(article_id)
    	       ON UPDATE CASCADE ON DELETE CASCADE,
    tag TEXT NOT NULL,
    created_on TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    user_name TEXT
);

INSERT INTO users(user_name)
VALUES
    ('Przemek G'), ('Agnieszka Z'), ('Elwira A');

CREATE TABLE articles_to_user_map(
    id SERIAL PRIMARY KEY,
    article_id INTEGER NOT NULL UNIQUE REFERENCES articles(article_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(user_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE UNIQUE INDEX user_result_uidx ON articles_to_user_map(article_id, user_id);

SELECT AM.article_id, U.user_name, A.*, S.service_name
    FROM articles_to_user_map AM
    JOIN users U USING(user_id)
    JOIN articles A USING(article_id)
    JOIN services S USING(service_id)
    WHERE S.service_name = 'dziennikwschodni';
