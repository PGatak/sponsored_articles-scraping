def add_start_urls(connection, start_urls):
    stmt = (
        """
        INSERT INTO start_urls(
            service_id,
            start_url_name
        )
        VALUES(
            (SELECT service_id FROM services
             WHERE service_name = %(service_name)s),
            %(start_url_name)s
        )
        ON CONFLICT (start_url_name) DO NOTHING
        RETURNING *
        """
    )

    with connection.cursor() as cur:
        for service_name, records in start_urls.items():
            for record in records:
                for key, link in record.items():
                    record = {"service_name": service_name,
                              "start_url_name": link}

                    cur.execute(stmt, record)
        cur.connection.commit()
        return cur.fetchall()


def get_start_urls(connection):
    stmt = (
        """
        SELECT S.service_name, SU.start_url_name
        FROM start_urls SU
        JOIN services S USING(service_id)
        """
    )

    with connection.cursor() as cur:
        cur.execute(stmt)
        return cur.fetchall()
#
# select AT.article_id, array_agg(AT.tag) AS tags, A.article_url from article_tags AT JOIN articles A ON A.article_id = AT.article_id group by AT.article_id, A.article_url;
