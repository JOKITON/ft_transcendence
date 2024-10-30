DOCKER_COMPOSE_LINUX = docker compose
DOCKER_COMPOSE_MAC =  docker-compose

# Check if docker-compose exists
DOCKER_COMPOSE_EXISTS := $(shell command -v docker-compose 2>/dev/null)
ifeq ($(DOCKER_COMPOSE_EXISTS),)
    DOCKER_COMPOSE_CMD = $(DOCKER_COMPOSE_LINUX)
else
    DOCKER_COMPOSE_CMD = $(DOCKER_COMPOSE_MAC)
endif

all:
	$(DOCKER_COMPOSE_CMD) -f docker-compose.yml up --build -d --remove-orphans

prod:
	$(DOCKER_COMPOSE_CMD) -f docker-compose-prod.yml up --build -d --remove-orphans


logs:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE) logs

logs-backend:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_BACKEND) logs

logs-metrics:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_METRICS) logs

clean:
	@$(DOCKER_COMPOSE_CMD)  down --remove-orphans --volumes
	#docker volume rm $(docker volume ls -qf dangling=true)
	
fclean: clean
	docker system prune --all --volumes --force

re: fclean all

info:
	@docker ps
	@docker images
	@docker volume ls
	@docker network ls
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE) ps
	@$(DOCKER_COMPOSE_CMD) -f $(COMPOSE) images

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

.PHONY: all  clean fclean re
