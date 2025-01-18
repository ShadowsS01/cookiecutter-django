# Cookiecutter Django

[![Build Status](https://img.shields.io/github/actions/workflow/status/dkshs/cookiecutter-django/ci.yml?branch=master)](https://github.com/dkshs/cookiecutter-django/actions/workflows/ci.yml?query=branch%3Amaster)
[![license mit](https://img.shields.io/badge/licence-MIT-56BEB8)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

> [!WARNING]
> Discontinued. See the [dkcutter-django](https://github.com/dkshs/dkcutter-django) project.

Powered by [Cookiecutter](https://github.com/cookiecutter/cookiecutter), Cookiecutter Django is a framework for jumpstarting production-ready Django projects quickly.

- If you have problems with Cookiecutter Django, please open [issues](https://github.com/dkshs/cookiecutter-django/issues/new).

## Usage

First, get Cookiecutter.

```bash
pip install cookiecutter
```

Now run it against this repo:

```bash
cookiecutter https://github.com/dkshs/cookiecutter-django
```

You'll be prompted for some values. Provide them, then a Django project will be created for you.

**Warning**: After this point, change 'DKSHS', etc to your own information.

Answer the prompts with your own desired [options](./docs/project-generation-options.md). For example:

```bash
# output
```

Enter the project and take a look around:

```bash
cd your_project_slug
ls
```

## For local development, see the following

- [Developing locally using docker](./docs/developing-locally-docker.md)

## References and inspirations

- [Cookiecutter](https://github.com/cookiecutter/cookiecutter) - A cross-platform command-line utility that creates projects from project templates, e.g. Python package projects, C projects.
- [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django) - A framework for jumpstarting production-ready Django projects quickly.

## License

This project is licensed under the **MIT** License - see the [LICENSE](./LICENSE) file for details
