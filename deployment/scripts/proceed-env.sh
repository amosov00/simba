#!/bin/bash

set -e

echo "########## Processing enviroment variables ##########"
cp "$ENV_BACKEND"           .env.backend
cp "$ENV_BACKEND_NODEJS"    .env.backend-nodejs
cp "$ENV_FRONTEND"          .env.frontend
cp "$ENV_DB"                .env.db
cp "$ENV_KAFKA"             .env.kafka


echo "########## Pass additional enviroment variables ##########"
touch .env
echo "CI_REGISTRY=$CI_REGISTRY
CI_PROJECT_NAMESPACE=$CI_PROJECT_NAMESPACE
CI_PROJECT_NAME=$CI_PROJECT_NAME
COMMIT=$CI_COMMIT_SHORT_SHA" >> .env
