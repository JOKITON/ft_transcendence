NAME = ft_transcendence

DOCKER = sudo docker-compose

DOCKER_IMAGES = $(addprefix ft_transcendence-,$(IMAGES))
DOCKER_IMAGES_BACKEND = $(addprefix ft_transcendence_backend-,$(IMAGES_BACKEND))
DOCKER_IMAGES_METRICS = $(addprefix ft_transcendence_metrics-,$(IMAGES_METRICS))

COMPOSE = src/compose/docker-compose.yml

COMPOSE_METRICS = src/compose/docker-compose-metrics.yml

COMPOSE_BACKEND = src/compose/docker-compose-backend.yml

VOLUMES = src/database/db  volumes/backend/jwt_auth_keys

.PHONY: all build down clean

all : up

$(VOLUMES) :
	@mkdir -p $(VOLUMES)

up : $(VOLUMES)
	# esto se puede definir con yaml mucho mejor
	$(DOCKER) -f $(COMPOSE) up --build -d  --remove-orphans
	$(DOCKER) -f $(COMPOSE_BACKEND) up --build -d  --remove-orphans
	#$(DOCKER) -f $(COMPOSE_METRICS) up --build -d  --remove-orphans

	
down:
	$(DOCKER) -f $(COMPOSE) down --volumes --remove-orphans --rmi all --remove-orphans
	$(DOCKER) -f $(COMPOSE_BACKEND) down --volumes --remove-orphans --rmi all --remove-orphans

logs:
	$(DOCKER) -f $(COMPOSE) logs


logs-backend:
	$(DOCKER) -f $(COMPOSE_BACKEND) logs

logs-metrics:
	$(DOCKER) -f $(COMPOSE_METRICS) logs

clean: down
	@sudo rm -rf $(VOLUMES)

fclean: clean
	sudo docker system prune --all --volumes --force
re: down up

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
