#!/usr/bin/env bash

# docker stop $(docker ps -q)
# ssh-keygen -R "[localhost]:2222"

docker build -t chall4 .
docker run -d --rm -p 2222:22 --name chall4 chall4

sleep 5
ssh -p2222 user@localhost
# ssh -p2222 -o "PubkeyAuthentication=no" -o "PasswordAuthentication=yes" user@localhost
