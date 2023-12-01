#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

readonly cmd="$*"

: "${POSTGRES_HOST:=postgres}"
: "${POSTGRES_PORT:=5432}"
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

: "${RABBITMQ_HOST:=rabbitmq}"
: "${RABBITMQ_PORT:=5672}"
export CLOUDAMQP_URL="amqp://${RABBITMQ_USER}:${RABBITMQ_PASSWORD}@${RABBITMQ_HOST}:${RABBITMQ_PORT}/${RABBITMQ_VHOST}"

# We need this line to make sure that this container is started after the one
# with PostgreSQL:
dockerize \
  -wait "tcp://${POSTGRES_HOST}:${POSTGRES_PORT}" \
  -wait "tcp://${RABBITMQ_HOST}:${RABBITMQ_PORT}" \
  -timeout 90s

>&2 echo 'PostgreSQL and RabbitMQ is up -- continuing...'

exec $cmd
