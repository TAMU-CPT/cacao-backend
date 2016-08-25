#!/bin/sh
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

# Start Gunicorn processes
echo Starting Gunicorn.
gunicorn cacao.wsgi:application \
	--name cacao_backend \
	--bind 0.0.0.0:8000 \
	--chdir=/app \
	--workers 3 \
	"$@"
