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

-- SELECT AM.article_id, U.user_name, A.*, S.service_name
--     FROM articles_to_user_map AM
--     JOIN users U USING(user_id)
--     JOIN articles A USING(article_id)
--     JOIN services S USING(service_id)
--     WHERE S.service_name = 'dziennikwschodni';


CREATE TABLE article_statuses(
    status_id SERIAL PRIMARY KEY,
    status TEXT NOT NULL UNIQUE
);


CREATE TABLE articles_to_status_map(
    id SERIAL PRIMARY KEY,
    article_id INTEGER NOT NULL UNIQUE REFERENCES articles(article_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    status_id INTEGER NOT NULL REFERENCES article_statuses(status_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE UNIQUE INDEX article_to_status_uidx ON articles_to_status_map(article_id, status_id);

INSERT INTO article_statuses(status) VALUES('Oferta'), ('Umowa'), ('Termin'), ('Fiasko'), ('Handlowiec');


CREATE OR REPLACE VIEW view_articles AS
       SELECT
		A.*,
		S.service_name,
		array_agg(AT.tag),
		U.user_id,
		U.user_name,
		AST.status,
		AST.status_id,
		DATE(A.created_on) AS date_created
        FROM articles A
            JOIN article_tags AT USING(article_id)
            JOIN services S USING(service_id)
        LEFT JOIN articles_to_user_map ATUM
             USING(article_id)
        LEFT JOIN articles_to_status_map ATSM
             USING(article_id)
        LEFT JOIN users U ON U.user_id = ATUM.user_id
        LEFT JOIN article_statuses AST ON AST.status_id = ATSM.status_id
        GROUP BY A.article_id,
          S.service_name,
          U.user_id,
          AST.status_id
        ORDER BY created_on DESC;


-- UNRELATED TO table users.
CREATE TABLE login_log(
       username TEXT PRIMARY KEY,
       counter INTEGER DEFAULT 0,
       mtime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION update_mtime()
       RETURNS TRIGGER
AS $$
   BEGIN
	NEW.mtime = NOW();
	RETURN NEW;
   END
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER trg_update_mtime BEFORE INSERT OR UPDATE
       ON login_log
       FOR EACH ROW EXECUTE PROCEDURE update_mtime();
