# Getting Up and Running Locally With Docker

## Prerequisites

- Docker; if you don't have it yet, follow the [installation instructions](https://docs.docker.com/get-docker/#supported-platforms).
- Docker Compose; refer to the official documentation for the [installation guide](https://docs.docker.com/compose/install/).
- Cookiecutter; refer to the official GitHub repository of [Cookiecutter](https://github.com/cookiecutter/cookiecutter).

## Before Getting Started

Generate a new django project:

```bash
cookiecutter --directory django https://github.com/ShadowsS01/templates
```

For more information refer to [Project Generation Options](./project-generation-options.md).

## Build the Stack

This can take a while, especially the first time you run this particular command on your development system:

```bash
docker-compose -f local.yml build
```

Generally, if you want to emulate production environment use `production.yml` instead. And this is true for any other actions you might need to perform: whenever a switch is required, just do it!

## Run the Stack

This brings up both Django, PostgreSQL and PGAdmin. The first time it is run it might take a while to get started, but subsequent runs will occur quickly.

Open a terminal at the project root and run the following for local development:

```bash
docker-compose -f local.yml up
```

You can also set the environment variable `COMPOSE_FILE` pointing to `local.yml` like this:

```bash
export COMPOSE_FILE=local.yml
```

And then run:

```bash
docker-compose up
```

To run in a detached (background) mode, just:

```bash
docker-compose up -d
```

The site should start and be accessible at <http://localhost:8000>.

## Execute Management Commands

As with any shell command that we wish to run in our container, this is done using the `docker-compose -f local.yml run --rm` command:

```bash
docker-compose -f local.yml run --rm django python manage.py migrate
docker-compose -f local.yml run --rm django python manage.py createsuperuser
```

Here, `django` is the target service we are executing the commands against.

## Configuring the Environment

This is the excerpt from your project’s `local.yml`:

```yml
# ...

postgres:
  build:
    context: .
    dockerfile: ./compose/production/postgres/Dockerfile
  volumes:
    - local_postgres_data:/var/lib/postgresql/data
    - local_postgres_data_backups:/backups
  env_file:
    - ./.envs/.local/.postgres
# ...
```

The most important thing for us here now is `env_file` section enlisting `./.envs/.local/.postgres`. Generally, the stack’s behavior is governed by a number of environment variables (env(s), for short) residing in `envs/`, for instance, this is what we generate for you:

```bash
.envs
├── .local
│   ├── .django
│   ├── .postgres
│   └── .pgadmin
└── .production
    ├── .django
    └── .postgres
```

Consider the aforementioned `.envs/.local/.postgres`:

```env
# PostgreSQL
# ------------------------------------------------------------------------------
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=<your project slug>
POSTGRES_USER=49nKf38fzX92JGfHjgpX5UyAv5RZ6q
POSTGRES_PASSWORD=awWYmw3K9b5m7WT62wxFySQY6wkgy25u3zHVT7NWJyCN9unuFbov69cuiL2U
```

The three envs we are presented with here are `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD` (by the way, their values have also been generated for you). You might have figured out already where these definitions will end up; it’s all the same with `django` service container envs.

## Tips & Tricks

### Add 3rd party python packages

To install a new 3rd party python package, you cannot use `pip install <package_name>`, that would only add the package to the container. The container is ephemeral, so that new library won’t be persisted if you run another container. Instead, you should modify the Docker image: You have to modify the relevant requirement file: base, local or production by adding:

```txt
<package_name>==<package_version>
```

To get this change picked up, you’ll need to rebuild the image(s) and restart the running container:

```bash
docker compose -f local.yml build
docker compose -f local.yml up
```

### Debugging

#### django-debug-toolbar

In order for `django-debug-toolbar` to work designate your Docker Machine IP with `INTERNAL_IPS` in `config/settings/local.py`.
