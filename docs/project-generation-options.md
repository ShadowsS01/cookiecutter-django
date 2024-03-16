# Project Generation Options

This page describes all the template options that will be prompted by the [cookiecutter CLI](https://github.com/cookiecutter/cookiecutter) prior to generating your project.

- **project_name**: Your project's human-readable name, capitals and spaces allowed.

- **project_slug**: Your project's slug without dashes or spaces. Used to name your repo and in other places where a Python-importable version of your project name is needed.

- **description**: Describes your project and gets used in places like README.md and such.

- **author_name**: This is you! The value goes into places like LICENSE and such.

- **domain_name**: The domain name you plan to use for your project once it goes live. Note that it can be safely changed later on whenever you need to.

- **email**: The email address you want to identify yourself in the project.

- **postgresql_version**: Select a [PostgreSQL](https://www.postgresql.org/docs/) version to use. The choices are:

  - 15
  - 14
  - 13
  - 12
  - 11
  - 10

- **cloud_provider**: Select a cloud provider for static & media files. The choices are:

  - [AWS](https://aws.amazon.com/s3/)
  - [GCP](https://cloud.google.com/storage)
  - None

  If you choose no cloud provider and docker, the production stack will serve the media files via an nginx Docker service. Without Docker, the media files won't work.

- **rest_framework**: Select a REST API framework. The choices are:

  - None
  - [DRF (Django REST framework)](https://www.django-rest-framework.org/)
  - [DNRF (Django Ninja REST framework)](https://django-ninja.rest-framework.com/)

- **mail_service**: Select an email service that Django-Anymail provides:

  - [Mailgun](https://www.mailgun.com/)
  - [Amazon SES](https://aws.amazon.com/ses/)
  - [Mailjet](https://www.mailjet.com/)
  - [Mandrill](http://mandrill.com/)
  - [Postmark](https://postmarkapp.com/)
  - [SendGrid](https://sendgrid.com/)
  - [SendinBlue](https://www.sendinblue.com/)
  - [SparkPost](https://www.sparkpost.com/)
  - [Other SMTP](https://anymail.readthedocs.io/en/stable/)
  - None

- **use_mailpit**: Indicates whether the project should be configured to use [Mailpit](https://github.com/axllent/mailpit/).

- **use_celery**: Indicates whether the project should be configured to use [Celery](https://github.com/celery/celery).

- **use_sentry**: Indicates whether the project should be configured to use [Sentry](https://github.com/getsentry/sentry).

- **use_whitenoise**: Indicates whether the project should be configured to use [WhiteNoise](https://github.com/evansd/whitenoise).

- **use_pgadmin**: Indicates whether the project should be configured to use [pgAdmin](https://www.pgadmin.org/).

- **use_tailwindcss**: Indicates whether the project should be configured to use [TailwindCSS](https://tailwindcss.com/).

- **automated_deps_updater**: select an automated dependency updater:

  - None
  - [Renovate](https://docs.renovatebot.com/)
  - [Dependabot](https://docs.github.com/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)
