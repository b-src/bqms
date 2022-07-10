.PHONY: test lint clean

DOCUMENT_DIR=temp/documents
DB_PATH=temp/bqms.db
MANUAL_TEST_ARTIFACTS=\
	$(DB_PATH)\
	$(DOCUMENT_DIR)/*

test:
	python3 bqms/main.py

lint:
	python3 -m black .
	python3 -m flakeheaven lint
	python3 -m mypy .

clean:
	rm -rf $(MANUAL_TEST_ARTIFACTS)