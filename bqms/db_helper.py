import sqlite3


DB_PATH = os.getenv('BQMS_DB_PATH')


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
    cursor = db_connection.cursor()
    cursor.execute(query, args)
    db_connection.commit()
    conn.close()
