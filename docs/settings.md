# Settings

For configuration purposes, the following table maps environment variables to their Django setting and project settings:

| Environment Variable                  | Django Setting              | Development Default | Production Default   |
| ------------------------------------- | --------------------------- | ------------------- | -------------------- |
| DATABASE_URL                          | DATABASES                   | auto w/ Docker;     | raises error         |
| DJANGO_ADMIN_URL                      | n/a                         | 'admin/'            | raises error         |
| DJANGO_DEBUG                          | DEBUG                       | True                | False                |
| DJANGO_SECRET_KEY                     | SECRET_KEY                  | auto-generated      | raises error         |
| DJANGO_ALLOWED_HOSTS                  | ALLOWED_HOSTS               | ['*']               | ['your_domain_name'] |
| DJANGO_SECURE_SSL_REDIRECT            | SECURE_SSL_REDIRECT         | n/a                 | True                 |
| DJANGO_SECURE_CONTENT_TYPE_NOSNIFF    | SECURE_CONTENT_TYPE_NOSNIFF | n/a                 | True                 |
| DJANGO_SECURE_FRAME_DENY              | SECURE_FRAME_DENY           | n/a                 | True                 |
| DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS | HSTS_INCLUDE_SUBDOMAINS     | n/a                 | True                 |
| DJANGO_SESSION_COOKIE_HTTPONLY        | SESSION_COOKIE_HTTPONLY     | n/a                 | True                 |
| DJANGO_SESSION_COOKIE_SECURE          | SESSION_COOKIE_SECURE       | n/a                 | False                |

The following table lists settings and their defaults for third-party applications, which may or may not be part of your project:

| Environment Variable           | Django Setting          | Development Default | Production Default |
| ------------------------------ | ----------------------- | ------------------- | ------------------ |
| DJANGO_AWS_ACCESS_KEY_ID       | AWS_ACCESS_KEY_ID       | n/a                 | raises error       |
| DJANGO_AWS_SECRET_ACCESS_KEY   | AWS_SECRET_ACCESS_KEY   | n/a                 | raises error       |
| DJANGO_AWS_STORAGE_BUCKET_NAME | AWS_STORAGE_BUCKET_NAME | n/a                 | raises error       |
| DJANGO_AWS_S3_REGION_NAME      | AWS_S3_REGION_NAME      | n/a                 | None               |
| DJANGO_AWS_S3_CUSTOM_DOMAIN    | AWS_S3_CUSTOM_DOMAIN    | n/a                 | None               |
| DJANGO_AWS_S3_MAX_MEMORY_SIZE  | AWS_S3_MAX_MEMORY_SIZE  | n/a                 | 100_000_000        |
| DJANGO_GCP_STORAGE_BUCKET_NAME | GS_BUCKET_NAME          | n/a                 | raises error       |
| GOOGLE_APPLICATION_CREDENTIALS | n/a                     | n/a                 | raises error       |
| SENTRY_DSN                     | SENTRY_DSN              | n/a                 | raises error       |
| SENTRY_ENVIRONMENT             | n/a                     | n/a                 | production         |
| SENTRY_TRACES_SAMPLE_RATE      | n/a                     | n/a                 | 0.0                |
| DJANGO_SENTRY_LOG_LEVEL        | SENTRY_LOG_LEVEL        | n/a                 | logging.INFO       |
