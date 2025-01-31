DOCKER_COMPOSE = docker-compose
API_CONTAINER=api-dev

debug:
	docker attach $(API_CONTAINER)
# Logs
logs:
	@$(DOCKER_COMPOSE) logs -f

# Docker Operations for Development
build-dev:
	@$(DOCKER_COMPOSE) --profile development build

up-dev:
	@$(DOCKER_COMPOSE) --profile development up

stop-dev:
	@$(DOCKER_COMPOSE) --profile development stop

down-dev:
	@$(DOCKER_COMPOSE) --profile development down

restart-dev:
	make build-dev && make down-dev -v && make up-dev

# Docker Operations for Production
build-prod:
	@$(DOCKER_COMPOSE) --profile production build

up-prod:
	@$(DOCKER_COMPOSE) --profile production up

stop-prod:
	@$(DOCKER_COMPOSE) --profile production stop

down-prod:
	@$(DOCKER_COMPOSE) --profile production down

restart-prod:
	make build-prod && make down-prod && make up-prod 
