import psycopg2
from psycopg2.extras import RealDictConnection
import os


DEFAULT_DSN = "dbname=%s" % os.environ.get("DBNAME", "artsql")


def create_connection(dsn=DEFAULT_DSN):
    return psycopg2.connect(
        dsn,
        connection_factory=RealDictConnection
    )
