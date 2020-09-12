def get_all_users(connection):
    stmt = "SELECT * FROM users"
    with connection.cursor() as cur:
        cur.execute(stmt)
        return cur.fetchall()


def assign_user_to_article(connection, user_id, article_id):
    STM_ADD_RESULT = (
        """
        INSERT INTO articles_to_user_map(user_id, articles_id)
        VALUES(%(user_id)s, %(articles_id)s)
        ON CONFLICT(article_id, user_id) DO NOTHING
        RETURNING *
        """
    )

    with connection.cursor() as cur:
        cur.execute(
            STM_ADD_RESULT,
            dict(
                user_id=user_id,
                article_id=article_id
            )
        )
        cur.connection.commit()
        return cur.fetchall()
