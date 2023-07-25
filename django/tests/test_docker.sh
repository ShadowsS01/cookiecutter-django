#!/bin/sh
# this is a very simple script that tests the docker configuration for cookiecutter-django
# it is meant to be run from the root directory of the repository, eg:
# sh tests/test_docker.sh

set -o errexit
set -x

# create a cache directory
mkdir -p .cache/docker
cd .cache/docker

# create the project using the default settings in cookiecutter.json
cookiecutter ../../ --no-input "$@"
cd my_awesome_project

# make sure all images build
docker compose -f local.yml build

# return non-zero status code if there are migrations that have not been created
docker compose -f local.yml run django python manage.py makemigrations --dry-run --check || {
  echo "ERROR: there were changes in the models, but migration listed above have not been created and are not saved in version control"
  exit 1
}

# Make sure the check doesn't raise any warnings
docker compose -f local.yml run django python manage.py check --fail-level WARNING
