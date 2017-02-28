# https://github.com/TAMU-CPT/docker-recipes/blob/master/django/Dockerfile.inherit
FROM quay.io/tamu_cpt/django

# Add our project to the /app/ folder
ADD . /app/
# Install dependencies
RUN pip install -r /app/requirements-prod.txt
# Set current working directory to /app
WORKDIR /app/

ENV DJANGO_WSGI_MODULE=cacao.wsgi \
	DJANGO_SETTINGS_MODULE=cacao.production
# Fix permissions on folder while still root, and collect static files for use
# if need be.
RUN chown -R django /app

# Drop permissions
USER django
