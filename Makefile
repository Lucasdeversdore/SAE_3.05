.PHONY: run
run:
	echo "nomDB = 'myapp.db'" > nomDB.py
	bash -c "source venv/bin/activate && flask run"

.PHONY: install
install:
	virtualenv -p python3 venv
	bash -c "source venv/bin/activate && pip install -r requirement.txt"

.PHONY: tests
tests:
	make loaddb_test 
	echo "nomDB = 'test.db'" > nomDB.py
	python -m unittest -v -b tests/test_*.py

.PHONY: pylint
pylint:
	pylint app test

.PHONY: loaddb
loaddb:
	echo "nomDB = 'myapp.db'" > nomDB.py
	sqlite3 myapp.db ".read script.sql"
	bash -c "source venv/bin/activate && flask loaddb bd.csv && flask newuser email.dev@gmail.com A1#45678 dev dev True && flask newuser etudiant@gmail.com A1#45678 etu etu False"
	

.PHONY: loaddb-test
loaddb_test:
	echo "nomDB = 'test.db'" > nomDB.py
	sqlite3 test.db ".read script.sql"
	bash -c "source venv/bin/activate && flask loaddb bd.csv && flask newuser email.dev@gmail.com A1#45678 dev dev True && flask newuser email.dev2@gmail.com A1#45678 dev2 dev2 True"
