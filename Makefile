NAME = ft_transcendence

DOCKER = sudo docker

# Variables
DOCKER_COMPOSE_LINUX = $(DOCKER) compose
DOCKER_COMPOSE_MAC = $(DOCKER)-compose

DOCKER_IMAGES = $(addprefix ft_transcendence-,$(IMAGES))
DOCKER_IMAGES_BACKEND = $(addprefix ft_transcendence_backend-,$(IMAGES_BACKEND))
DOCKER_IMAGES_METRICS = $(addprefix ft_transcendence_metrics-,$(IMAGES_METRICS))
# Add here the container names
IMAGES = frontend proxy
IMAGES_BACKEND = keys admin pong db auth migration friendship
IMAGES_METRICS = grafana prometheus

# Check if docker-compose exists
DOCKER_COMPOSE_EXISTS := $(shell command -v docker-compose 2>/dev/null)

# Conditional command assignment
ifeq ($(DOCKER_COMPOSE_EXISTS),)
    DOCKER_COMPOSE_CMD = $(DOCKER_COMPOSE_LINUX)
else
    DOCKER_COMPOSE_CMD = $(DOCKER_COMPOSE_MAC)
endif

COMPOSE = src/compose/docker-compose.yml

COMPOSE_METRICS = src/compose/docker-compose-metrics.yml

COMPOSE_BACKEND = src/compose/docker-compose-backend.yml

VOLUMES = volumes/db volumes/dependencies

.PHONY: all build down clean $(NETWORKS)

all : up

$(NETWORKS) :
	@$(DOCKER) network inspect proxy >/dev/null 2>&1 || $(DOCKER) network create proxy && echo "Created metrics network."

$(VOLUMES) :
	@mkdir -p $(VOLUMES)

up : $(NETWORKS) $(VOLUMES)
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE) up --build -d  --remove-orphans

logs:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE) logs

logs-backend:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_BACKEND) logs

logs-metrics:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_METRICS) logs

down:
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE) down --remove-orphans --volumes
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_BACKEND) down --remove-orphans --volumes

clean:
	@$(DOCKER) rmi -f $(DOCKER_IMAGES)
	@$(DOCKER) rmi -f $(DOCKER_IMAGES_BACKEND)
	@$(DOCKER) rmi -f $(DOCKER_IMAGES_METRICS)
	rm -rf networks
	sudo rm -rf volumes/
	@$(DOCKER) network prune --force
	@$(DOCKER) image prune --force

fclean: down clean
	@$(DOCKER) system prune --all --volumes --force

re: down up
