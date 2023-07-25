# Deployment with Docker

## Prerequisites

- Docker 17.05+.
- Docker Compose 1.17+

## Building & Running Production Stack

You will need to build the stack first. To do that, run:

```bash
docker-compose -f production.yml build
```

Once this is ready, you can run it with:

```bash
docker-compose -f production.yml up
```

To run the stack and detach the containers, run:

```bash
docker-compose -f production.yml up -d
```

To run a migration, open up a second terminal and run:

```bash
docker-compose -f production.yml run --rm django python manage.py migrate
```

To create a superuser, run:

```bash
docker-compose -f production.yml run --rm django python manage.py createsuperuser
```

## Media files without cloud provider

The media files will be served by an nginx service, from a `production_django_media` volume. Make sure to keep this around to avoid losing any media files.
