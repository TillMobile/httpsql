#!/usr/bin/env bash

cd /opt/

# Set ENV
. .env

# Start the DB
sudo service postgresql start

# Start the WSGI server
source venv/bin/activate
nohup gunicorn httpsql.api:app --bind=127.0.0.1:8000 &

# Load fixture data
export PGPASSWORD=$DB_PASSWORD
psql -h $DB_HOST -d $DB_DATABASE -U $DB_USER -p $DB_PORT -a -w -f /opt/test/fixtures/item.sql

sleep 5

# Run tests
cd /opt/test/
python test.py