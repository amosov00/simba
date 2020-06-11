#!/usr/bin/env sh

set -e

echo "########## Processing enviroment variables ##########"
test -n "$ENV_BACKEND" || echo Fatal : missing file ENV_BACKEND
test -n "$ENV_FRONTEND" || echo Fatal : missing file ENV_FRONTEND
test -n "$ENV_DB" || echo Fatal : missing file ENV_DB

cp "$ENV_BACKEND" .env.backend
cp "$ENV_FRONTEND" .env.frontend
cp "$ENV_DB" .env.db


echo "########## Pass additional enviroment variables ##########"
# COMMIT SHA for SENTRY
echo "$CI_COMMIT_SHORT_SHA" >> .env.backend
echo "$CI_COMMIT_SHORT_SHA" >> .env.frontend
