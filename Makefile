.PHONY: help
MODELS:=$(wildcard */models.py)

help:
	@egrep '^[a-zA-Z_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test: ## Run tests
	python manage.py test

fixtures:  ## Load fixtures for base set of apps
	python manage.py migrate
	python manage.py loaddata fixtures/00_auth.json
	python manage.py loaddata fixtures/00_directory.json
	python manage.py shell < fixtures/drop.py
	python manage.py loaddata fixtures/01_account.json

sync: ## Make migrations
	python manage.py makemigrations
	python manage.py migrate

run: ## Run the server
	python manage.py runserver

models.png: $(MODELS) ## Build PNG file of database models
	python manage.py graph_models -a -o models.png

.PHONY: help test fixtures sync run
