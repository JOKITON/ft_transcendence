NAME = ft_transcendence

DOCKER_COMPOSE = docker-compose
COMPOSE_YML = docker-compose.yml

.PHONY: all build down clean

all : up

up :
	$(DOCKER_COMPOSE) -f $(COMPOSE_YML) up --build

down:
	$(DOCKER_COMPOSE) -f $(COMPOSE_YML) down

clean:
	$(DOCKER_COMPOSE) -f $(COMPOSE_YML) down -v

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
