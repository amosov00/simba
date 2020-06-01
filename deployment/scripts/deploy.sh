#!/usr/bin/env sh

set -e

>.env

echo "CI_REGISTRY=$CI_REGISTRY" >> .env.local
echo "CI_PROJECT_NAMESPACE=$CI_PROJECT_NAMESPACE" >> .env.local
echo "CI_PROJECT_NAME=$CI_PROJECT_NAME" >> .env.local


echo "########## Processing enviroment and pems ##########"
if [[ "$CI_COMMIT_REF_SLUG" == "master" ]]; then
    DOCKER_COMPOSE_FILENAME="docker-compose.prod.yml"
    HOST_IP=$PROD_HOST_IP
    PROJECT_DIR='/home/projects/neutrinobank'
    HOST_USER=root
    cp ./deployment/permissions/neutrino.pem ./permission.pem

elif [[ "$CI_COMMIT_REF_SLUG" == "develop" ]]; then
    DOCKER_COMPOSE_FILENAME="docker-compose.develop.yml"
    HOST_IP=$DEVELOP_HOST_IP
    PROJECT_DIR='/home/netwood/_projects/neutrinobank'
    HOST_USER=nikita
    echo "$HETZNER_DEV_HOST_1_PEM" >> ./permission.pem
else
    DOCKER_COMPOSE_FILENAME="docker-compose.yml"
fi

chmod 400 ./permission.pem

echo "########## Using '$DOCKER_COMPOSE_FILENAME' config ##########"
echo "########## Ping $HOST_IP with settings $SSH_OPTION ##########"
ssh $SSH_OPTION -i ./permission.pem $HOST_USER@"$HOST_IP"

echo "########## Pull changes from gitlab repo ##########"
ssh $SSH_OPTION -i ./permission.pem $HOST_USER@"$HOST_IP" "cd $PROJECT_DIR &&
git pull https://$DEPLOY_TOKEN_USERNAME:$DEPLOY_TOKEN_SECRET@gitlab.com/$CI_PROJECT_NAMESPACE/$CI_PROJECT_NAME $CI_COMMIT_REF_NAME"

echo "########## Copy .env file ##########"
scp $SSH_OPTION -i ./permission.pem ./.env $HOST_USER@"$HOST_IP":$PROJECT_DIR

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