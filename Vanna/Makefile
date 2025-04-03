# Variáveis configuráveis
include .env
export

ID ?= 1
REGISTRY = $(REGISTRY)
USER = $(USER)
IMAGE_NAME = $(REGISTRY)/$(USER)/banco
TAG = latest

COMPOSE = docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml --env-file .env

up:
	$(COMPOSE) up --build -d
down:
	$(COMPOSE) down -v
prd-up:
	docker-compose -f docker-compose.yaml -f docker-compose.prd.yaml --env-file .env.prd up -d
prd-down:
	docker-compose -f docker-compose.yaml -f docker-compose.prd.yaml --env-file .env.prd down -v

restart-banco:
	$(COMPOSE) restart banco

redo-banco:
	$(COMPOSE) stop banco
	$(COMPOSE) rm -f banco
	$(COMPOSE) build banco
	$(COMPOSE) up -d banco

logs-banco:
	$(COMPOSE) logs -f banco

prdlogs-banco:
	docker-compose -f docker-compose.yaml -f docker-compose.prd.yaml --env-file .env.prd logs -f banco

build-prd-banco:
	docker build -t $(IMAGE_NAME):$(TAG) ./services/banco

push-gitea-banco: build-prd-banco
	docker push $(IMAGE_NAME):$(TAG)

restart-mqtt:
	$(COMPOSE) restart mqtt

redo-mqtt:
	$(COMPOSE) stop mqtt
	$(COMPOSE) rm -f mqtt
	$(COMPOSE) build mqtt
	$(COMPOSE) up -d mqtt

logs-mqtt:
	$(COMPOSE) logs -f mqtt

prdlogs-mqtt:
	docker-compose -f docker-compose.yaml -f docker-compose.prd.yaml --env-file .env.prd logs -f mqtt

build-prd-mqtt:
	docker build -t $(IMAGE_NAME):$(TAG) ./services/mqtt

push-gitea-mqtt: build-prd-mqtt
	docker push $(IMAGE_NAME):$(TAG)

restart-ingestion:
	$(COMPOSE) restart ingestion

redo-ingestion:
	$(COMPOSE) stop ingestion
	$(COMPOSE) rm -f ingestion
	$(COMPOSE) build ingestion
	$(COMPOSE) up -d ingestion

logs-ingestion:
	$(COMPOSE) logs -f ingestion

prdlogs-ingestion:
	docker-compose -f docker-compose.yaml -f docker-compose.prd.yaml --env-file .env.prd logs -f ingestion

build-prd-ingestion:
	docker build -t $(IMAGE_NAME):$(TAG) ./services/ingestion

push-gitea-ingestion: build-prd-ingestion
	docker push $(IMAGE_NAME):$(TAG)

restart-retrieval:
	$(COMPOSE) restart retrieval

redo-retrieval:
	$(COMPOSE) stop retrieval
	$(COMPOSE) rm -f retrieval
	$(COMPOSE) build retrieval
	$(COMPOSE) up -d retrieval

logs-retrieval:
	$(COMPOSE) logs -f retrieval

prdlogs-retrieval:
	docker-compose -f docker-compose.yaml -f docker-compose.prd.yaml --env-file .env.prd logs -f retrieval

build-prd-retrieval:
	docker build -t $(IMAGE_NAME):$(TAG) ./services/retrieval

push-gitea-retrieval: build-prd-retrieval
	docker push $(IMAGE_NAME):$(TAG)

start-camera:
	mosquitto_pub -h $(MQTT_BROKER_ADDRESS) -t commands/$(ID) -m "start"
stop-camera:
	mosquitto_pub -h $(MQTT_BROKER_ADDRESS) -t commands/$(ID) -m "stop"

local-tests: test-unit test-integration
test-unit:
	PYTHONPATH=. pytest tests/unit --disable-warnings -v
test-integration:
	PYTHONPATH=. pytest tests/integration --disable-warnings -v
