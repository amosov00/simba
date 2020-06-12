#!/bin/bash

echo "########## Deploying to server ##########"

echo "########## Check is folder is created ##########"
ssh "$SSH_USER"@"$SSH_HOST" "cd '$PROJECT_DIR' || mkdir -p '$PROJECT_DIR'"

echo "########## Pull changes from gitlab repo ##########"
ssh "$SSH_USER"@"$SSH_HOST" "cd '$PROJECT_DIR' && git pull $CI_REPOSITORY_URL $CI_COMMIT_REF_NAME"

echo "########## Pull images from Gitlab Container Registry ##########"
ssh "$SSH_USER"@"$SSH_HOST" "docker login -u '$CI_REGISTRY_USER' -p $CI_REGISTRY_PASSWORD $CI_REGISTRY"
ssh "$SSH_USER"@"$SSH_HOST" "cd '$PROJECT_DIR' && docker-compose -f $DOCKER_COMPOSE_FILENAME pull"
ssh "$SSH_USER"@"$SSH_HOST" "docker logout $CI_REGISTRY"

echo "########## Copy .env files ##########"
scp .env          "$SSH_USER"@"$SSH_HOST":"$PROJECT_DIR"
scp .env.backend  "$SSH_USER"@"$SSH_HOST":"$PROJECT_DIR"
scp .env.frontend "$SSH_USER"@"$SSH_HOST":"$PROJECT_DIR"
scp .env.db       "$SSH_USER"@"$SSH_HOST":"$PROJECT_DIR"
scp .env.rabbitmq "$SSH_USER"@"$SSH_HOST":"$PROJECT_DIR"


echo "########## Reload containers services ##########"
ssh "$SSH_USER"@"$SSH_HOST" "cd '$PROJECT_DIR' && docker-compose -f $DOCKER_COMPOSE_FILENAME up -d"

echo "########## Remove docker <none> images ##########"
ssh "$SSH_USER"@"$SSH_HOST" 'docker rmi $(docker images --filter "dangling=true" -q --no-trunc)' || echo "Docker none images is not found"