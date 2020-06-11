#!/bin/bash
echo "########## Processing ssh file ##########"

test -n "$SSH_USER" || echo Fatal : missing variable SSH_PRIVATE_KEY
test -n "$SSH_HOST" || echo Fatal : missing variable SSH_PRIVATE_KEY
test -n "$SSH_PRIVATE_KEY" || echo Fatal : missing variable SSH_PRIVATE_KEY
test -n "$SSH_KNOWN_HOSTS" || echo Warn : missing variable SSH_KNOWN_HOSTS

export SSH_OPTION="123"

which ssh-agent || ( apt-get update -y && apt-get install openssh-client -y )

eval $(ssh-agent -s)
echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add - > /dev/null
mkdir -p ~/.ssh
chmod 700 ~/.ssh

if [ -n "$SSH_KNOWN_HOSTS" ]; then
    ssh-keyscan -H "$SSH_KNOWN_HOSTS" > ~/.ssh/known_hosts
    chmod 644 ~/.ssh/known_hosts
fi
