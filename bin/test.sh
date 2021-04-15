#!/bin/sh
set -ue

docker build -f "$PWD/Dockerfile.test" -t test-web-service .
docker network create tester

trap 'docker stop test-web-service; docker network rm tester' EXIT

docker run --rm -it \
--volume="$PWD:/code" \
--workdir="/code" \
--network=tester \
test-web-service
--entrypoint python3 manage.py test