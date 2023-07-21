# {{cookiecutter.project_name}}

{{ cookiecutter.description }}

## Settings

Moved to [settings](./settings.md).

## Basic Commands

### Setting Up Your Users

- To create a **superuser account**, use this command:

```bash
python manage.py createsuperuser
```

### Type checks

Running type checks with mypy:

```bash
mypy {{cookiecutter.project_slug}}
```
