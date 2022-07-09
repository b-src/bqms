import os
from uuid import uuid4

import db_helper
from git_helper import GitHelper


class DocumentManager:
    def __init__(self):
        self.document_root_dir = os.getenv("BQMS_DOCUMENT_ROOT")
        self.git_helper = GitHelper()
        
    def create_new_document(self, document_name) -> bool:
        result = False
        # TODO: check there are no document name collisions
        document_dir = uuid4().hex
        full_path = os.path.join(self.document_root_dir, document_dir)
        if os.path.exists(full_path):
            raise Exception("UUID document dir collision somehow")
        
        # TODO: handle exceptions
        os.makedirs(full_path)
        
        # TODO: handle failures
        self.git_helper.git_init(full_path)
        
        record_inserted_successfully = db_helper.insert_document_record(document_name, document_dir)
        
        result = True
        return result
        
        
        
        

