from db_init import initialize_database
from document_manager import DocumentManager


if __name__ == "__main__":
    initialize_database()
    document_manager = DocumentManager()

    document_manager.create_new_document("test_document")
