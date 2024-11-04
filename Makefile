.PHONY: run
run:
	bash -c "source venv/bin/activate && flask run"

.PHONY: install
install:
	virtualenv -p python3 venv
	bash -c "source venv/bin/activate && pip install -r requirement.txt"

.PHONY: tests
tests:  
	python -m unittest -v -b test/test_*.py

.PHONY: pylint
pylint:
	pylint app test

.PHONY: loaddb
loaddb:
	sqlite3 myapp.db ".read script.sql"
	bash -c "source venv/bin/activate && flask loaddb bd.csv"

