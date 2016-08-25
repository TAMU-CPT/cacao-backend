#!/bin/bash

postgres_ready() {
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="postgres")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."

python manage.py migrate

cat > create_admin.py << END
#!/usr/bin/env python
import random, string, sys, os
sys.path.append(os.getcwd())
import django
django.setup()
from django.contrib.auth.models import User
password  = "".join([random.SystemRandom().choice(string.digits + string.letters) for i in range(32)])

try:
	u = User.objects.create_superuser('admin', 'admin@localhost', password)
	u.save()
except:
	u = User.objects.filter(username='admin')[0]
	u.set_password(password)

print "\n\nSeting admin password to %s\n\n" % password
END
python create_admin.py

# Start Gunicorn processes
echo Starting Gunicorn.
gunicorn cacao.wsgi:application \
	--bind 0.0.0.0:8000 \
	--workers 3 \
	"$@"
