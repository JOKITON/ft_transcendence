NAME = ft_transcendence

# Variables
DOCKER_COMPOSE_LINUX = docker compose
DOCKER_COMPOSE_MAC = docker-compose

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

clean:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_YML) down -v

# Help target
help:
	@echo "Usage: make [TARGET]"
	@echo ""
	@echo "Targets:"
	@echo "  all       : Build and start the containers (default)"
	@echo "  up		   : Build and start the Docker containers"
	@echo "  down      : Stop and remove the Docker containers"
	@echo "  clean     : Clean up the Docker volumes"
	@echo "  help      : Show this help message"
