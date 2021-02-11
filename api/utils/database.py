import os
import psycopg2

def get_database_connection():
    return psycopg2.connect(
        dbname=os.environ[f"PGDATABASE"],
        user=os.environ[f"PGUSER"],
        password=os.environ[f"PGPASSWORD"],
        host=os.environ[f"PGHOST"]
    )

def get_database_cursor(connection=None):
    if connection:
        return connection.cursor()

    return get_database_connection().cursor()