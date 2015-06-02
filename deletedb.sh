#!/bin/bash
rm db.sqlite3
rm vendors/migrations/0001_initial.p*
python manage.py sqlflush | python manage.py dbshell
python manage.py makemigrations vendors
python manage.py sqlmigrate vendors 0001
python manage.py migrate
python manage.py shell < create_test_entries.txt
