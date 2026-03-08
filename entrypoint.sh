#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
while ! python -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(('db', 5432))
    s.close()
    exit(0)
except:
    exit(1)
" 2>/dev/null; do
    echo "  Postgres not ready yet, retrying in 1s..."
    sleep 1
done

echo "PostgreSQL is up - running seed and starting app"

# Run seed script to populate data
python seed.py

# Start the application
exec gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 "app:create_app()"
