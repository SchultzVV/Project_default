# Variáveis configuráveis
include .env
export

ID ?= 1
REGISTRY = registry.gitea.seuservidor.com
USER = seu-usuario
IMAGE_NAME = $(REGISTRY)/$(USER)/storage
TAG = latest

COMPOSE = docker compose -f docker-compose.yaml -f docker-compose.dev.yaml --env-file .env

up:
	$(COMPOSE) up --build -d
down:
	$(COMPOSE) down -v
prd-up:
	docker compose -f docker-compose.yaml -f docker-compose.prd.yaml --env-file .env.prd up -d
prd-down:
	docker compose -f docker-compose.yaml -f docker-compose.prd.yaml --env-file .env.prd down -v

restart-storage:
	$(COMPOSE) restart storage

redo-storage:
	$(COMPOSE) stop storage
	$(COMPOSE) rm -f storage
	$(COMPOSE) build storage
	$(COMPOSE) up -d storage

logs-storage:
	$(COMPOSE) logs -f storage

prdlogs-storage:
	docker compose -f docker-compose.yaml -f docker-compose.prd.yaml --env-file .env.prd logs -f storage

build-prd-storage:
	docker build -t $(IMAGE_NAME):$(TAG) ./services/storage

push-gitea-storage: build-prd-storage
	docker push $(IMAGE_NAME):$(TAG)

restart-system_of_classification:
	$(COMPOSE) restart system_of_classification

redo-system_of_classification:
	$(COMPOSE) stop system_of_classification
	$(COMPOSE) rm -f system_of_classification
	$(COMPOSE) build system_of_classification
	$(COMPOSE) up -d system_of_classification

logs-system_of_classification:
	$(COMPOSE) logs -f system_of_classification

prdlogs-system_of_classification:
	docker compose -f docker-compose.yaml -f docker-compose.prd.yaml --env-file .env.prd logs -f system_of_classification

build-prd-system_of_classification:
	docker build -t $(IMAGE_NAME):$(TAG) ./services/system_of_classification

push-gitea-system_of_classification: build-prd-system_of_classification
	docker push $(IMAGE_NAME):$(TAG)

local-tests: test-unit test-integration
test-unit:
	PYTHONPATH=. pytest tests/unit --disable-warnings -v
test-integration:
	PYTHONPATH=. pytest tests/integration --disable-warnings -v
