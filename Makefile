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
	
down:
	$(DOCKER) -f $(COMPOSE) down --volumes --remove-orphans --rmi all

logs:
	$(DOCKER) -f $(COMPOSE) logs


logs-backend:
	$(DOCKER) -f $(COMPOSE_BACKEND) logs

logs-metrics:
	$(DOCKER) -f $(COMPOSE_METRICS) logs

clean:
	@$(DOCKER) rmi -f $(DOCKER_IMAGES)
	@$(DOCKER) rmi -f $(DOCKER_IMAGES_BACKEND)
	@$(DOCKER) rmi -f $(DOCKER_IMAGES_METRICS)
	@$(DOCKER) network prune --force
	@$(DOCKER) image prune --force
	@sudo rm -rf $(VOLUMES)

re: down up

curl: 
	curl -X POST \
		http://localhost/api/pong/rounds/ \
	 -H 'Content-Type: application/json' \
  -d '{ "player1": "1", "player2": "2", "score1": 10, "score2": 8 }'

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
