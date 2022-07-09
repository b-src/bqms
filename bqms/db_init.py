import os
import sqlite3


DB_PATH = os.getenv("BQMS_DB_PATH")


CREATE_TABLE_DOCUMENTS = """
CREATE TABLE documents (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
dir_path TEXT NOT NULL
)
"""


def execute_table_create_statement(
    db_connection: sqlite3.Connection, table_create_statement: str
) -> None:
    cursor = db_connection.cursor()

    cursor.execute(table_create_statement)

    db_connection.commit()


def initialize_database() -> None:
    if DB_PATH is None:
        raise Exception("BQMS_DB_PATH env var not set")

    conn = sqlite3.connect(DB_PATH)

    execute_table_create_statement(conn, CREATE_TABLE_DOCUMENTS)

    conn.close()
