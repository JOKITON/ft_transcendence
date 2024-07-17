NAME = ft_transcendence

# Variables
DOCKER_COMPOSE_LINUX = sudo docker compose
DOCKER_COMPOSE_MAC = sudo docker-compose

DOCKER_IMAGES = $(addprefix ft_transcendence-,$(IMAGES))
# Add here the container names
IMAGES = proxy app db vue

# Check if docker-compose exists
DOCKER_COMPOSE_EXISTS := $(shell command -v docker-compose 2>/dev/null)

# Conditional command assignment
ifeq ($(DOCKER_COMPOSE_EXISTS),)
    DOCKER_COMPOSE_CMD = $(DOCKER_COMPOSE_LINUX)
else
    DOCKER_COMPOSE_CMD = $(DOCKER_COMPOSE_MAC)
endif

COMPOSE_BACK = src/compose/docker-compose-backend.yml
COMPOSE_FRONT = src/compose/docker-compose-frontend.yml
COMPOSE_MONI = src/compose/docker-compose-monitoring.yml
COMPOSE_UTILS = src/compose/docker-compose-utils.yml
COMPOSE = src/compose/docker-compose.yml

.PHONY: all build down clean

all : up

up :
	$(DOCKER_COMPOSE_CMD) --env-file ./src/database/.env.dev  -f  $(COMPOSE_UTILS) -f  $(COMPOSE_BACK) -f $(COMPOSE_FRONT) -f $(COMPOSE_MONI) up --build -d  --remove-orphans
down:
	$(DOCKER_COMPOSE_CMD) --env-file ./src/database/.env.dev  -f  $(COMPOSE_UTILS) -f  $(COMPOSE_BACK) -f $(COMPOSE_FRONT) -f $(COMPOSE_MONI) down --volumes 
clean:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_YML) down -v
	sudo docker rmi $(DOCKER_IMAGES)

re: down  up

info:
	@sudo docker ps
	@sudo docker images
	@sudo docker volume ls
	@sudo docker network ls
	@sudo $(DOCKER_COMPOSE_CMD) ps
	@sudo $(DOCKER_COMPOSE_CMD) images

curl: 
	curl -X POST \
		http://localhost/api/pong/rounds/ \
	 -H 'Content-Type: application/json' \
  -d '{ "player1": "1", "player2": "2", "score1": 10, "score2": 8 }'
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
