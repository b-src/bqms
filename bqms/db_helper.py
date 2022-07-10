import os
import sqlite3


# TODO: create App class to manage globals and do this properly
DB_PATH = str(os.getenv("BQMS_DB_PATH"))


def get_document_id_from_dir_path(dir_path: str) -> int:
    query = """
    SELECT id FROM documents
    WHERE dir_path = ?;
    """
    args = (dir_path,)

    result = execute_parameterized_select_statement(query, args)[0][0]

    return result


def get_document_dir_path_from_id(document_id: int) -> str:
    query = """
    SELECT name FROM documents
    WHERE id = ?;
    """
    args = (document_id,)

    result = execute_parameterized_select_statement(query, args)[0][0]

    return result


def insert_document_record(document_name: str, dir_path: str) -> bool:
    query = """
    INSERT INTO documents (name, dir_path)
    VALUES (?, ?);
    """
    args = (document_name, dir_path)

    # TODO: is this the inserted id as expected?
    result = execute_parameterized_insert_statement(query, args)[0]

    return result


def insert_revision_record(document_id: int, version: str) -> int:
    query = """
    INSERT INTO revisions (document_id, version)
    VALUES (?, ?);
    """
    args = (document_id, version)

    result = execute_parameterized_insert_statement(query, args)

    return result


def update_document_revision(document_id: int, revision_id: int) -> bool:
    query = """
    UPDATE documents
    SET current_revision_id = ? 
    WHERE id = ?
    """
    args = (revision_id, document_id)

    # TODO: is this a bool as expected?
    result = execute_parameterized_update_statement(query, args)[0]

    return result


# TODO: verify how this is being returned
def execute_parameterized_select_statement(query: str, args: tuple) -> tuple:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    result = cursor.execute(query, args)
    conn.close()

    return bool(result)


# TODO: verify how this is being returned
def execute_parameterized_insert_statement(query: str, args: tuple) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    result = cursor.execute(query, args)
    conn.commit()
    conn.close()

    return result


# TODO: verify how this is being returned
def execute_parameterized_update_statement(query: str, args: tuple) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    result = cursor.execute(query, args)
    conn.close()

    return bool(result)
