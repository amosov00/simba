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

test -n "$ENV_BACKEND" || echo Fatal : missing file ENV_BACKEND
test -n "$ENV_FRONTEND" || echo Fatal : missing file ENV_FRONTEND
test -n "$ENV_DB" || echo Fatal : missing file ENV_DB
test -n "$SSH_USER" || echo Fatal : missing variable SSH_USER
test -n "$SSH_HOST" || echo Fatal : missing variable SSH_HOST
test -n "$SSH_PRIVATE_KEY" || echo Fatal : missing variable SSH_PRIVATE_KEY
test -n "$SSH_KNOWN_HOSTS" || echo Fatal : missing variable SSH_KNOWN_HOSTS
test -n "$PROJECT_DIR" || echo Fatal : missing variable PROJECT_DIR
test -n "$DOCKER_COMPOSE_FILENAME" || echo Fatal : missing variable DOCKER_COMPOSE_FILENAME
test -n "$CI_ENVIRONMENT_SLUG" || echo Fatal : missing variable CI_ENVIRONMENT_SLUG