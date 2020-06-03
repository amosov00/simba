#!/usr/bin/env sh

set -e

>.env

echo "CI_REGISTRY=$CI_REGISTRY" >> .env
echo "CI_PROJECT_NAMESPACE=$CI_PROJECT_NAMESPACE" >> .env
echo "CI_PROJECT_NAME=$CI_PROJECT_NAME" >> .env


echo "########## Processing enviroment and pems ##########"
if [[ "$CI_COMMIT_REF_NAME" == "master" ]]; then
    DOCKER_COMPOSE_FILENAME="docker-compose.prod.yml"
    HOST_IP=$PROD_HOST_IP
    PROJECT_DIR=''
    HOST_USER=root

elif [[ "$CI_COMMIT_REF_NAME" == "develop" ]]; then
    DOCKER_COMPOSE_FILENAME="docker-compose.develop.yml"
    HOST_IP=91.132.23.151
    PROJECT_DIR='/home/netwood/_projects/simba'
    HOST_USER=nikita
    echo "$HETZNER_DEV_HOST_1_PEM" >> ./permission.pem
fi

chmod 400 ./permission.pem


echo "########## Using '$DOCKER_COMPOSE_FILENAME' config ##########"
echo "########## Ping $HOST_IP with settings $SSH_OPTION ##########"
ssh $SSH_OPTION -i ./permission.pem $HOST_USER@"$HOST_IP"

echo "########## Pull changes from gitlab repo ##########"
ssh $SSH_OPTION -i ./permission.pem $HOST_USER@"$HOST_IP" "cd $PROJECT_DIR && git pull $CI_REPOSITORY_URL $CI_COMMIT_REF_NAME"

echo "########## Copy .env files ##########"
scp $SSH_OPTION -i ./permission.pem ./.env $HOST_USER@"$HOST_IP":$PROJECT_DIR

#ssh $SSH_OPTION -i ./permission.pem $HOST_USER@"$HOST_IP" "cd $PROJECT_DIR &&
#'$ENV_BACKEND' > .env.backend && '$ENV_DB' > .env.db && '$ENV_FRONTEND' > .env.frontend"

echo "########## Pull images from Gitlab Container Registry ##########"
ssh $SSH_OPTION -i ./permission.pem $HOST_USER@"$HOST_IP" "docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY"

ssh $SSH_OPTION -i ./permission.pem $HOST_USER@"$HOST_IP" "cd $PROJECT_DIR &&
docker-compose -f ./$DOCKER_COMPOSE_FILENAME pull"

echo "########## Start services ##########"
ssh $SSH_OPTION -i ./permission.pem $HOST_USER@"$HOST_IP" "cd $PROJECT_DIR &&
docker-compose -f ./$DOCKER_COMPOSE_FILENAME up -d"

echo "########## Remove docker <none> images ##########"
ssh $SSH_OPTION -i ./permission.pem $HOST_USER@"$HOST_IP" 'docker rmi $(docker images --filter "dangling=true" -q --no-trunc)' ||
echo "Docker none images is not found"