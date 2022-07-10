import os
from uuid import uuid4

import db_helper
from git_helper import GitHelper


class DocumentManager:
    def __init__(self):
        self.document_root_dir = os.getenv("BQMS_DOCUMENT_ROOT")
        self.git_helper = GitHelper()

    def create_new_document(self, document_name: str) -> bool:
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

        record_inserted_successfully = db_helper.insert_document_record(
            document_name, document_dir
        )

        result = True
        return result and record_inserted_successfully

    def create_draft_revision(self, document_id: int, revision_name) -> bool:
        result = False

        document_dir = db_helper.get_document_dir_path_from_id(document_id)
        result = self.git_helper.git_create_branch(dir_path)

        return result

    def save_changes_to_document(
        self, document_source_path: str, document_dest_path: str
    ) -> bool:
        # TODO: right now this takes the path of a document as input. this will
        # eventually have to be updated to accomodate whatever method the API uses to
        # accept input document data
        if os.path.exists(document_dest_path):
            os.remove(document_dest_path)

        with open(document_source_path, mode="r") as doc_input:
            with open(document_dest_path, mode="x") as doc_output:
                doc_data = doc_input.read()
                doc_output.write(doc_data)

        filename = os.path.basename(document_dest_path)
        dir_name = os.path.dirname(document_dest_path)

        self.git_helper.git_add(dir_name, filename)
        self.git_helper.git_commit(dir_name, "placeholder dummy message")

        # TODO: figure out what actually happened
        return True

    def publish_changes_to_document(self, document_dir, revision_name, new_version):
        checkout_successful = self.git_helper.git_check_out_existing_branch(
            document_dir, "main"
        )
        merge_successful = self.git_helper.git_merge(document_dir, revision_name)

        document_id = db_helper.get_document_id_from_dir_path(document_dir)

        revision_id = db_helper.insert_revision_record(document_id, new_version)

        document_revision_updated = db_helper.update_document_revision(
            document_id, revision_id
        )

        result = checkout_successful and merge_successful and document_revision_updated
