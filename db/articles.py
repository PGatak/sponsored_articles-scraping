def add_article(connection, record):
    stmt = (
        """
        INSERT INTO articles(
            service_id,
            article_url
        )
        VALUES(
            (SELECT service_id FROM services
             WHERE service_name = %(service_name)s),
            %(article_url)s
        )
        ON CONFLICT (article_url) DO NOTHING
        RETURNING *
        """

    )
    with connection.cursor() as cur:
        cur.execute(stmt, record)
        cur.connection.commit()
        return cur.fetchone()


def get_articles(connection):
    stmt = (
        """
        SELECT S.service_name, A.article_url
        FROM articles A
        JOIN services S USING(service_id)
        """
    )

    with connection.cursor() as cur:
        cur.execute(stmt)
        return cur.fetchall()


def remove_article(connection, article):
    stmt = (
        """
        DELETE FROM article
        WHERE article_url = %(article_url)s
        RETURNING *
        """
    )
    with connection.cursor() as cur:
        cur.execute(stmt, article)
        cur.connection.commit()
        return cur.fetchall()


def add_new_articles(connection, record):
    stmt = (
        """
        INSERT INTO new_articles(
            service_id,
            article_url
        )
        VALUES(
            (SELECT service_id FROM services
            WHERE service_name = %(service_name)s),
            %(article_url)s
        )
        ON CONFLICT (article_url) DO NOTHING
        RETURNING *
        """
        )
    with connection.cursor() as cur:
        cur.execute(stmt, record)
        cur.connection.commit()
        return cur.fetchall()


def get_new_articles(connection):
    stmt = (
        """
        SELECT S.service_name, NA.article_url
        FROM new_articles NA
        JOIN services S USING(service_id)
        """
    )

    with connection.cursor() as cur:
        cur.execute(stmt)
        return cur.fetchall()


def get_articles_by_service_name(connection, service_name):
    stmt = (
        """
        SELECT * FROM articles A
        JOIN services S USING(service_id)
        WHERE S.service_name = %s
        """
    )
    with connection.cursor() as cur:
        cur.execute(stmt, (service_name,))
        return cur.fetchall()


def is_article_old(connection, article):
    stmt = (
        """
        SELECT count(*) AS cnt FROM articles
        WHERE article_url = %(article_url)s
        """
    )
    with connection.cursor() as cur:
        cur.execute(stmt, article)
        cnt = cur.fetchone()["cnt"]
        return cnt


def add_article_tags(connection, article_id, tags):
    stmt = (
        """
        INSERT INTO article_tags(article_id, tag)
        VALUES(%(article_id)s, %(tag)s)
        """
    )

    with connection.cursor() as cur:
        for tag in tags:
            cur.execute(stmt, dict(article_id=article_id, tag=tag))
        cur.connection.commit()

