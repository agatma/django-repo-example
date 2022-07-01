.DEFAULT_GOAL := help

.PHONY: help
help:  ## List all commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

OVERRIDE=`test -f deploy/docker-compose.override.yml && \
		  echo '-f deploy/docker-compose.override.yml'`

.PHONY: lock-deps
lock-deps:  ## Make poetry.lock
	docker-compose \
		-f deploy/docker-compose.yml \
		-f deploy/docker-compose.develop.yml \
		${OVERRIDE} \
		--project-directory . \
		run --rm example-app poetry lock

.PHONY: shell
shell:  ## Shell (bash) into the app's container
	docker-compose \
		-f deploy/docker-compose.yml \
		-f deploy/docker-compose.db.yml \
		-f deploy/docker-compose.develop.yml \
		${OVERRIDE} \
		--project-directory . \
		run --rm example-app bash

.PHONY: test
test:  ## Start project's tests in docker
	docker-compose \
		-f deploy/docker-compose.yml \
		-f deploy/docker-compose.db.yml \
		-f deploy/docker-compose.tests.yml \
		${OVERRIDE} \
		--project-directory . \
		run --rm example-app-tests

.PHONY: lint
lint:  ## Start project's lint in docker
	docker-compose \
	    -f deploy/docker-compose.yml \
	    ${OVERRIDE} \
	    --project-directory . \
	    run --rm example-app \
	        flake8 --count

.PHONY: build
build:  ## Build docker image
	docker-compose \
		-f deploy/docker-compose.yml \
		${OVERRIDE} \
		--project-directory . \
		build example-app

.PHONY: envfile
envfile:  ## Generate env file with variables with prefix EXAMPLE_
	$(shell env | egrep '^EXAMPLE_' > .gen.env && echo '.gen.env has been generated' || touch .gen.env)
	$(shell test -f .env && cat .env > .gen.env)

runserver:  envfile  ## Local startup the app in docker with required services
	docker-compose \
		-f deploy/docker-compose.yml \
		-f deploy/docker-compose.db.yml \
		-f deploy/docker-compose.develop.yml \
		${OVERRIDE} \
		--project-directory . \
		up

runserver-gunicorn:  envfile  ## Local startup the app in docker with gunicorn/uvicorn
	docker-compose \
		-f deploy/docker-compose.yml \
		-f deploy/docker-compose.db.yml \
		${OVERRIDE} \
		--project-directory . \
		up
