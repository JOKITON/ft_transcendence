NAME = ft_transcendence

DOCKER = sudo docker

# Variables
DOCKER_COMPOSE_LINUX = $(DOCKER) compose
DOCKER_COMPOSE_MAC = $(DOCKER)-compose

DOCKER_IMAGES = $(addprefix ft_transcendence-,$(IMAGES))
DOCKER_IMAGES_BACKEND = $(addprefix ft_transcendence_backend-,$(IMAGES_BACKEND))
DOCKER_IMAGES_METRICS = $(addprefix ft_transcendence_metrics-,$(IMAGES_METRICS))
# Add here the container names
IMAGES = frontend reverse-proxy
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

NETWORKS = networks/frontend networks/metrics

VOLUMES = volumes/db volumes/dependencies

.PHONY: all build down clean

all : up

$(NETWORKS) :
	@$(DOCKER) network create metrics
	@$(DOCKER) network create frontend
	mkdir networks
	touch $(NETWORKS)

$(VOLUMES) :
	@mkdir -p $(VOLUMES)

up : $(NETWORKS) $(VOLUMES)
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_BACKEND) up --build -d  --remove-orphans
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE) up --build -d  --remove-orphans
	# $(DOCKER_COMPOSE_CMD) -f $(COMPOSE_METRICS) up --build -d  --remove-orphans
logs:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE) logs
logs-backend:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_BACKEND) logs
logs-metrics:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_METRICS) logs
down:
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE) down --volumes
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_BACKEND) down --volumes
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_METRICS) down --volumes
	rm -rf networks
	sudo rm -rf volumes/
	@$(DOCKER) network rm metrics frontend
clean:
	@$(DOCKER) rmi -f $(DOCKER_IMAGES)
	@$(DOCKER) rmi -f $(DOCKER_IMAGES_BACKEND)
	@$(DOCKER) rmi -f $(DOCKER_IMAGES_METRICS)
	@$(DOCKER) network prune --force
	@$(DOCKER) image prune --force
fclean:
	@$(DOCKER) system prune --force
	@$(DOCKER) volume rm $(sudo docker volume ls -q)
	@$(DOCKER) rmi $(sudo docker images -q)
	@$(DOCKER) rm $(sudo docker ps -qa)

re: down clean up

curl: 
	curl -X POST \
		http://localhost/api/login \
	 -H 'Content-Type: application/json' \
	 -d '{ "username": "admin", "password": "admin"}'

info:
	@sudo docker ps
	@sudo docker images
	@sudo docker volume ls
	@sudo docker network ls
	@sudo $(DOCKER_COMPOSE_CMD) -f $(COMPOSE) ps
	@sudo $(DOCKER_COMPOSE_CMD) -f $(COMPOSE_BACKEND) ps
	@sudo $(DOCKER_COMPOSE_CMD) -f $(COMPOSE_METRICS) ps
	@sudo $(DOCKER_COMPOSE_CMD) -f $(COMPOSE) images
	@sudo $(DOCKER_COMPOSE_CMD) -f $(COMPOSE_BACKEND) images
	@sudo $(DOCKER_COMPOSE_CMD) -f $(COMPOSE_METRICS) images

# Help target
help:
	@echo "Usage: make [TARGET]"
	@echo ""
	@echo "Targets:"
	@echo "  all       : Build and start the containers (default)"
	@echo "  up		   : Build and start the Docker containers"
	@echo "  down      : Stop and remove the Docker containers"
	@echo "  clean     : Clean up the Docker volumes"
	@echo "  info      : List information about containers"
	@echo "  help      : Show this help message"
	@echo "  re        : Redoes the whole project"