#!/usr/bin/env bash

while ! pg_isready -q -h $PGHOST -p $PGPORT -U $PGUSER
do
  echo "$(date) - waiting for database to start"
  sleep 2
done

if [[ -z `psql -Atqc "\\list $PGDATABASE"` ]]; then
  echo "Database $PGDATABASE does not exist. Creating..."
  createdb -E UTF8 $PGDATABASE -l en_US.UTF-8 -T template0
  echo "Database $PGDATABASE created."
fi

if [[ -z `psql -Atqc "\\list $PGDATABASETEST"` ]]; then
  echo "Database $PGDATABASETEST does not exist. Creating..."
  createdb -E UTF8 $PGDATABASETEST -l en_US.UTF-8 -T template0
  echo "Database $PGDATABASETEST created."
fi

echo "-- RUNNING SQL SCRIPTS --"
psql -d $PGDATABASE -a -f sql/quote.sql -q

echo db init
python manage.py db init
echo db migrate
python manage.py db migrate
echo db upgrade
python manage.py db upgrade

python -W ignore manage.py test

uwsgi app.ini