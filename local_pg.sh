#!/bin/sh

docker rm -f pg ||:
docker run -d -p 5432:5432 --name pg -e POSTGRES_PASSWORD=azerty -e POSTGRES_USER=test -e POSTGRES_DB=test-db postgres:14-alpine
docker logs -f pg
