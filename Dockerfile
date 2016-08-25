FROM python:2.7-alpine

# Update the default application repository sources list
RUN apk update && \
	apk add postgresql-dev gcc python3-dev musl-dev

ADD requirements-prod.txt /app/requirements-prod.txt
WORKDIR /app
RUN pip --no-cache-dir install -r requirements-prod.txt && \
	addgroup -S django && \
	adduser -S -G django django
ADD . /app
RUN chown -R django /app
# Port to expose
EXPOSE 8000
# Copy entrypoint script into the image
USER django
ENTRYPOINT ["/app/docker-entrypoint.sh"]
