DOCKER_COMPOSE_LINUX = docker compose
DOCKER_COMPOSE_MAC = docker-compose

# Check if docker-compose exists
DOCKER_COMPOSE_EXISTS := $(shell command -v docker-compose 2>/dev/null)
ifeq ($(DOCKER_COMPOSE_EXISTS),)
    DOCKER_COMPOSE_CMD = $(DOCKER_COMPOSE_LINUX)
else
    DOCKER_COMPOSE_CMD = $(DOCKER_COMPOSE_MAC)
endif

all:
	$(DOCKER_COMPOSE_CMD) -f docker-compose.yml up --build -d --remove-orphans

clean:
	@$(DOCKER_COMPOSE_CMD)  down --remove-orphans --volumes
	#docker volume rm $(docker volume ls -qf dangling=true)
	
fclean: clean
	bash ./scripts/clean.sh
	docker system prune --all --volumes --force

fclean-sudo: clean
	rm -rf ${USER}
	bash ./scripts/clean.sh
	docker system prune --all --volumes --force

re: fclean all

.PHONY: all  clean fclean re
