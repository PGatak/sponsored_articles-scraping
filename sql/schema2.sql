
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
