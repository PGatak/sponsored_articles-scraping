def add_services(connection, all_start_urls):
    stmt = (
        """
        INSERT INTO services(
            service_name
        )
        VALUES(
            %(service_name)s
        )
        ON CONFLICT (service_name) DO NOTHING
        RETURNING *
        """
    )
    with connection.cursor() as cur:
        for name in all_start_urls:
            record = {"service_name": name}
            cur.execute(stmt, record)
        cur.connection.commit()
        return cur.fetchall()
