#!/bin/bash
rm db.sqlite3
rm vendors/migrations/0001_initial.p*
python3 manage.py sqlflush | python3 manage.py dbshell
python3 manage.py makemigrations vendors
python3 manage.py sqlmigrate vendors 0001
python3 manage.py migrate
python3 manage.py shell < create_test_entries.txt
