# Settings

For configuration purposes, the following table maps environment variables to their Django setting and project settings:

| Environment Variable                  | Django Setting              | Development Default                         | Production Default |
|---------------------------------------|-----------------------------|---------------------------------------------|--------------------|
| DATABASE_URL                          | DATABASES                   | auto w/ Docker;                             | raises error       |
| DJANGO_ADMIN_URL                      | n/a                         | 'admin/'                                    | raises error
| DJANGO_DEBUG                          | DEBUG                       | True                                        | False
| DJANGO_SECRET_KEY                     | SECRET_KEY                  | auto-generated                              | raises error
| DJANGO_ALLOWED_HOSTS                  | ALLOWED_HOSTS               | ['*']                                       | ['your_domain_name']
| DJANGO_SECURE_SSL_REDIRECT            | SECURE_SSL_REDIRECT         | n/a                                         | True
| DJANGO_SECURE_CONTENT_TYPE_NOSNIFF    | SECURE_CONTENT_TYPE_NOSNIFF | n/a                                         | True
| DJANGO_SECURE_FRAME_DENY              | SECURE_FRAME_DENY           | n/a                                         | True
| DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS | HSTS_INCLUDE_SUBDOMAINS     | n/a                                         | True
| DJANGO_SESSION_COOKIE_HTTPONLY        | SESSION_COOKIE_HTTPONLY     | n/a                                         | True
| DJANGO_SESSION_COOKIE_SECURE          | SESSION_COOKIE_SECURE       | n/a                                         | False
