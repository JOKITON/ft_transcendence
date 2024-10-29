DOCKER_COMPOSE_LINUX = docker compose
DOCKER_COMPOSE_MAC =  docker-compose

# Check if docker-compose exists
DOCKER_COMPOSE_EXISTS := $(shell command -v docker-compose 2>/dev/null)
ifeq ($(DOCKER_COMPOSE_EXISTS),)
    DOCKER_COMPOSE_CMD = $(DOCKER_COMPOSE_LINUX)
else
    DOCKER_COMPOSE_CMD = $(DOCKER_COMPOSE_MAC)
endif

VOLUMES = ${USER}/volumes/db ${USER}/volumes/dependencies ${USER}/volumes/redis \
	${USER}/volumes/proxy ${USER}/volumes/frontend ${USER}/volumes/db  ${USER}/volumes/pong \
	${USER}/volumes/friendship ${USER}/volumes/auth ${USER}/volumes/livechat


all:
	@mkdir -p $(VOLUMES)
	$(DOCKER_COMPOSE_CMD) -f docker-compose.yml up --build -d --remove-orphans

front:
	$(DOCKER_COMPOSE_CMD) -f docker-compose.yml.prod up --build -d --remove-orphans frontend

logs:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE) logs

logs-backend:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_BACKEND) logs

logs-metrics:
	$(DOCKER_COMPOSE_CMD) -f $(COMPOSE_METRICS) logs

clean:
	sudo rm -rf $(USER)
	@$(DOCKER_COMPOSE_CMD)  down --remove-orphans --volumes
	#docker volume rm $(docker volume ls -qf dangling=true)
	
fclean: clean
	docker system prune --all --volumes --force

re: fclean all

.PHONY: all  clean fclean re
