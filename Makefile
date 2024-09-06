#---------------------------- Transcendence ----------------------------#

# Variables
NAME			= transcendence
LOGIN			= $(if $(SUDO_USER),$(SUDO_USER),$(shell whoami))
SRCS			= ./srcs
COMPOSE			= $(SRCS)/docker-compose.yml
HOST_URL		= 127.0.0.1
OS              = $(shell uname -s)
HOME_PATH       = $(if $(filter $(OS),Darwin),/Users/$(LOGIN),/home/$(LOGIN))
DATABASE_PATH   = $(HOME_PATH)/data/postgresql
PROMETHEUS_PATH = $(HOME_PATH)/data/prometheus
GRAFANA_PATH    = $(HOME_PATH)/data/grafana

#---------------------------- Rules ----------------------------#

# Development mode
dev: setup_folder
	@docker compose -f $(COMPOSE) up --watch

# Start the application in detached mode (in the background)
## -f : Specify an alternate compose file (here a path)
## -d : Detached mode: Run containers in the background
## --build : Force Rebuild of images before starting containers
up: setup_folder
	@/bin/bash -c '\
		if [ ! -f ./srcs/.env ]; then \
			echo "❌ Credentials files not found! 🔑" && exit 1; \
		fi; \
		'
	@docker compose -f $(COMPOSE) up -d --build

# Start the application
start:
	@docker compose -f $(COMPOSE) start

# Stop the application
stop:
	@docker compose -f $(COMPOSE) stop

# Stop and remove containers, networks created by 'up'
down:
	@docker compose -f $(COMPOSE) down

# Remove containers, networks, volumes, and images created by 'up'
clean:
	@docker compose -f $(COMPOSE) down --rmi all --volumes 

# Additional cleaning, remove all unused containers, networks, and images
fclean: clean
	@docker system prune -af

#---------------------------- Django ----------------------------#

# Check Deployment
django_check_deploy:
	@docker compose -f $(COMPOSE) exec django python manage.py check --deploy

#---------------------------- Docker ----------------------------#

# Check Compose file
config:
	@docker compose -f $(COMPOSE) config

#---------------------------- Files Management ----------------------------#

# Create the necessary folders
setup_folder:
	@mkdir -p $(DATABASE_PATH)
	@mkdir -p $(PROMETHEUS_PATH)
	@mkdir -p $(GRAFANA_PATH)

# Delete the data base folder
.PHONY: delete_db_folder
delete_db_folder:
	@rm -r $(DATABASE_PATH)

# Delete the prometheus folder
.PHONY: delete_prometheus_folder
delete_prometheus_folder:
	@rm -r $(PROMETHEUS_PATH)

# Delete the grafana folder
.PHONY: delete_grafana_folder
delete_grafana_folder:
	@rm -r $(GRAFANA_PATH)

#---------------------------- DNS Custom ----------------------------#

# Add the host url to the /etc/hosts file (requires sudo) for DNS resolution
.PHONY: add_url
add_url:
	@sudo sed -i '/$(HOST_URL)/d' /etc/hosts # Remove the previous entry if it exists
	@echo "127.0.0.1 $(HOST_URL)" | sudo tee -a /etc/hosts # Add the new entry

# Remove the host url from the /etc/hosts file (requires sudo)
.PHONY: remove_url
remove_url:
	@sudo sed -i '/$(HOST_URL)/d' /etc/hosts

#---------------------------- Credentials ----------------------------#

# Create empty credentials files from templates
template:
	@/bin/bash -c '\
		if [ -f ./srcs/.env ]; then \
			echo "❌ Credentials files already exist! 🔑" && exit 1; \
			exit 0; \
		fi; \
		if [ "$$EUID" -eq 0 ]; then \
			echo "❌ Please run this command without sudo! 🔑" && exit 1; \
		fi; \
		for file in ./secrets/*.template; do \
			cp $$file "$${file%.template}"; \
		done; \
		cp ./srcs/.env.template ./srcs/.env && \
		sed -i '/^LOGIN=.*/c\LOGIN=$(LOGIN)' ./srcs/.env && \
		sed -i '/^HOME_PATH=.*/c\HOME_PATH=$(HOME_PATH)' ./srcs/.env && \
		echo "✔️ Credentials files are ready! 🔑" \
		'

# Remove credentials files
rm_secrets:
	@/bin/bash -c '\
		echo "Do you want to remove your secrets [Y/N] ?" && read answer; \
		if [[ $$answer =~ ^[Yy] ]]; then \
			for file in ./secrets/*.txt ; do \
				rm -f "$$file"; \
			done ;\
			rm -f ./srcs/.env; \
			echo "✔️ Credentials files are removed! 🔑"; \
		fi;\
		'

#---------------------------- Help ----------------------------#

# Set the default goal to the help message
.DEFAULT_GOAL := help

# Display the help message
help:
	@echo "$(PROGRAM)Usage:$(RESET)"
	@echo "  make $(EXEC)up$(RESET)         - Build and start the services"
	@echo "  make $(EXEC)down$(RESET)       - Stop and remove containers and networks of the services"
	@echo "  make $(EXEC)start$(RESET)      - Start the services"
	@echo "  make $(EXEC)stop$(RESET)       - Stop the services"
	@echo "  make $(EXEC)clean$(RESET)      - Remove containers, networks, volumes, and images"
	@echo "  make $(EXEC)fclean$(RESET)     - Additional cleaning, remove all unused containers, networks, and images"
	@echo "  make $(EXEC)infos$(RESET)      - Display information about the services"
	@echo "  make $(EXEC)logs$(RESET)       - Display the logs of the services"
	@echo "  make $(COMPILED)dev$(RESET)        - Start the services in development mode (watch)"
	@echo "  make $(EXEC)config$(RESET)     - Check the Compose file (fill in the variables)"
	@echo "  make $(EXEC)add_url$(RESET)    - Add $(HOST_URL) to the /etc/hosts file"
	@echo "  make $(EXEC)remove_url$(RESET) - Remove $(HOST_URL) from the /etc/hosts file"
	@echo "  make $(EXEC)template$(RESET)   - Create empty credentials files from templates"
	@echo "  make $(EXEC)rm_secrets$(RESET) - Remove credentials files"
	@echo "  make $(EXEC)shell_<container>$(RESET) - Access the shell of a container"
	@echo "  make $(EXEC)help$(RESET)       - Display this help message"

# Display information about the application
infos:
	@clear
	@echo "\n---------------------{ 🗃️  CONTAINERS }---------------------"
	@docker ps -a
	@echo "\n-----------------------{ 🖼️  IMAGES }-----------------------"
	@docker image ls --filter "reference=$(NAME)*"
	@echo "\n-----------------------{ 💾 VOLUMES }----------------------"
	@docker volume ls --filter "name=$(NAME)"
	@echo "\n-----------------------{ 🌐 NETWORKS }---------------------"
	@docker network ls --filter "name=$(NAME)"
	@echo ""

#---------------------------- Logs ----------------------------#

# Display the logs of the application
## logs -f : Follow log output (streaming) (Ctrl+C to exit)
logs:
	@docker compose -f $(COMPOSE) logs -f

## nginx logs
logs_nginx:
	@docker exec nginx tail -f /var/log/nginx/access.log

## django container logs
log_django:
	@docker compose -f $(COMPOSE) logs -f django

#---------------------------- Shell ----------------------------#

# Access PostgreSQL container
.PHONY: shell_postgresql
shell_postgresql:
	@docker exec -it postgresql /bin/bash

# Access Django container
.PHONY: shell_django
shell_django:
	@docker exec -it django /bin/bash

# Access Nginx container
.PHONY: shell_nginx
shell_nginx:
	@docker exec -it nginx /bin/bash

# Access Redis container
.PHONY: shell_redis
shell_redis:
	@docker exec -it redis /bin/bash

# Access Prometheus container
.PHONY: shell_prometheus
shell_prometheus:
	@docker exec -it prometheus /bin/bash

# Access Grafana container
.PHONY: shell_grafana
shell_grafana:
	@docker exec -it grafana /bin/bash

# Access Alertmanager container
.PHONY: shell_alertmanager
shell_alertmanager:
	@docker exec -it alertmanager /bin/sh

#---------------------------- Phony ----------------------------#

.PHONY: start stop clean fclean help infos logs logs_nginx dev up down

#---------------------------- Specials ----------------------------#

# Hide the output of commands
HIDE = > /dev/null 2>&1

#---------------------------- Colors ----------------------------#

# ANSI escape codes for colors and formatting
# Format: \033[<attribute>;<foreground>;<background>m

EXEC = \033[1;94m
PROGRAM = \033[4;1;95m
COMPILED = \033[1;92m
ARCHIVED = \033[2;93m
FAILED = \033[1;31m
SUCCESS = \033[1;32m

# Attributes (0 to 7)
RESET = \033[0m
BOLD = \033[1m
DIM = \033[2m
UNDERLINE = \033[4m
REVERSED = \033[7m

# Foreground Colors (30 to 37)
BLACK = \033[0;30m
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[0;33m
BLUE = \033[0;34m
PURPLE = \033[0;35m
CYAN = \033[0;36m
WHITE = \033[0;37m

GREY = \033[38;5;240m

# Highlight (Bright) Foreground Colors (90 to 97)
BRIGHT_BLACK = \033[0;90m
BRIGHT_RED = \033[0;91m
BRIGHT_GREEN = \033[0;92m
BRIGHT_YELLOW = \033[0;93m
BRIGHT_BLUE = \033[0;94m
BRIGHT_PURPLE = \033[0;95m
BRIGHT_CYAN = \033[0;96m
BRIGHT_WHITE = \033[0;97m

# Background Colors (40 to 47)
BG_BLACK = \033[0;40m
BG_RED = \033[0;41m
BG_GREEN = \033[0;42m
BG_YELLOW = \033[0;43m
BG_BLUE = \033[0;44m
BG_PURPLE = \033[0;45m
BG_CYAN = \033[0;46m
BG_WHITE = \033[0;47m

# Highlight (Bright) Background Colors (100 to 107)
BG_BRIGHT_BLACK = \033[0;100m
BG_BRIGHT_RED = \033[0;101m
BG_BRIGHT_GREEN = \033[0;102m
BG_BRIGHT_YELLOW = \033[0;103m
BG_BRIGHT_BLUE = \033[0;104m
BG_BRIGHT_PURPLE = \033[0;105m
BG_BRIGHT_CYAN = \033[0;106m
BG_BRIGHT_WHITE = \033[0;107m

