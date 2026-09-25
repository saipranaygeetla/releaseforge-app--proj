import os

import psycopg


DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", "5432"))
DATABASE_NAME = os.getenv("DATABASE_NAME", "releaseforge")
DATABASE_USER = os.getenv("DATABASE_USER", "releaseforge")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")


def get_connection():
    return psycopg.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        dbname=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
    )