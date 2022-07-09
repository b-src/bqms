import os
import sqlite3


# TODO: create App class to manage globals and do this properly
DB_PATH = str(os.getenv("BQMS_DB_PATH"))


def insert_document_record(document_name, dir_path) -> bool:
    query = """
    INSERT INTO documents (name, dir_path)
    VALUES (?, ?);
    """
    args = (document_name, dir_path)

    result = execute_parameterized_insert_statement(query, args)

    return result


def execute_parameterized_insert_statement(query: str, args: tuple) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    result = cursor.execute(query, args)
    conn.commit()
    conn.close()

    # TODO: convert this properly. for now this silences mypy
    return bool(result)
