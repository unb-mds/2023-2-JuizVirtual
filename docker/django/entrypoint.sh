#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

readonly cmd="$*"

: "${POSTGRES_HOST:=postgres}"
: "${POSTGRES_PORT:=5432}"
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

# We need this line to make sure that this container is started after the one
# with PostgreSQL:
dockerize \
  -wait "tcp://${POSTGRES_HOST}:${POSTGRES_PORT}" \
  -timeout 90s

>&2 echo 'PostgreSQL is up -- continuing...'

exec $cmd
