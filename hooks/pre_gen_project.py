from __future__ import print_function

import sys

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
ERROR = "\x1b[1;31m [ERROR]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

# The content of this string is evaluated by Jinja, and plays an important role.
# It updates the cookiecutter context to trim leading and trailing spaces
# from domain/email values
"""
{{ cookiecutter.update({ "domain_name": cookiecutter.domain_name | trim }) }}
{{ cookiecutter.update({ "email": cookiecutter.email | trim }) }}
"""

project_slug = "{{ cookiecutter.project_slug }}"
if hasattr(project_slug, "isidentifier"):
    assert (
        project_slug.isidentifier()
    ), f"{ERROR}'{project_slug}' project slug is not a valid Python identifier.{TERMINATOR}"

assert (
    project_slug == project_slug.lower()
), f"{ERROR}'{project_slug}' project slug should be all lowercase{TERMINATOR}"

assert "\\" not in "{{ cookiecutter.author_name }}", f"{ERROR}Don't include backslashes in author name.{TERMINATOR}"

if "{{ cookiecutter.use_whitenoise }}".lower() == "n" and "{{ cookiecutter.cloud_provider }}" == "None":
    print(f"{ERROR}You should either use Whitenoise or select a " f"Cloud Provider to serve static files{TERMINATOR}")
    sys.exit(1)

if "{{ cookiecutter.mail_service }}" == "Amazon SES" and "{{ cookiecutter.cloud_provider }}" != "AWS":
    print(f"{ERROR}You should either use AWS or select a different " f"Mail Service for sending emails.{TERMINATOR}")
    sys.exit(1)

if "{{ cookiecutter.mail_service }}" == "None" and "{{ cookiecutter.use_mailpit }}".lower() == "y":
    print(f"{ERROR}You should not use mailpit without an email service.{TERMINATOR}")
    sys.exit(1)
