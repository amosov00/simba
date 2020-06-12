#!/bin/bash

set -e

echo "########## Testing env variables ##########"

#declare -a variables_arr=(
#"ENV_BACKEND" "ENV_FRONTEND" "ENV_DB"
#"SSH_USER" "SSH_HOST" "SSH_PRIVATE_KEY" "SSH_KNOWN_HOSTS"
#"PROJECT_DIR" "DOCKER_COMPOSE_FILENAME" "CI_ENVIRONMENT_SLUG"
#)
#
#for i in "${variables_arr[@]}"
#do
#  if [[ -z "$i" ]]; then
#    echo "missing env $i"
#  fi
##  echo {!var}
##  test -n "$var" || echo Fatal : missing env "var"
#done

test -n "$ENV_BACKEND" || echo Fatal : missing file ENV_BACKEND && exit 1
test -n "$ENV_FRONTEND" || echo Fatal : missing file ENV_FRONTEND && exit 1
test -n "$ENV_DB" || echo Fatal : missing file ENV_DB && exit 1
test -n "$ENV_RABBITMQ" || echo Fatal : missing file ENV_RABBITMQ && exit 1
test -n "$SSH_USER" || echo Fatal : missing variable SSH_USER && exit 1
test -n "$SSH_HOST" || echo Fatal : missing variable SSH_HOST && exit 1
test -n "$SSH_PRIVATE_KEY" || echo Fatal : missing variable SSH_PRIVATE_KEY && exit 1
test -n "$SSH_KNOWN_HOSTS" || echo Fatal : missing variable SSH_KNOWN_HOSTS && exit 1
test -n "$PROJECT_DIR" || echo Fatal : missing variable PROJECT_DIR && exit 1
test -n "$DOCKER_COMPOSE_FILENAME" || echo Fatal : missing variable DOCKER_COMPOSE_FILENAME && exit 1
test -n "$CI_ENVIRONMENT_SLUG" || echo Fatal : missing variable CI_ENVIRONMENT_SLUG && exit 1