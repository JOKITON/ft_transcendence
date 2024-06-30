NAME = ft_transcendence

# Variables
DOCKER_COMPOSE_LINUX = docker compose
DOCKER_COMPOSE_MAC = docker-compose

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

COMPOSE_YML = docker-compose.yml

.PHONY: all build down clean

all : up

up :
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_YML) up --build

down:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_YML) down
	sudo docker rmi $(DOCKER_IMAGES)

clean:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_YML) down -v

re: down clean up

info:
	@sudo docker ps
	@sudo docker images
	@sudo docker volume ls
	@sudo docker network ls
	@sudo $(DOCKER_COMPOSE_CMD) ps
	@sudo $(DOCKER_COMPOSE_CMD) images

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
