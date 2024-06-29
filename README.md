# Django Template

[![Build Status](https://img.shields.io/github/actions/workflow/status/dkshs/cookiecutter-django/ci.yml?branch=master)](https://github.com/dkshs/cookiecutter-django/actions/workflows/ci.yml?query=branch%3Amaster)
[![license mit](https://img.shields.io/badge/licence-MIT-56BEB8)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

A simple Django template with cookiecutter.

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
