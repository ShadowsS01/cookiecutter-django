from http import HTTPStatus

import pytest
from django.urls import reverse


def test_swagger_accessible_by_admin(admin_client):
    {%- if cookiecutter.rest_framework == 'DRF' %}
    url = reverse("api-docs")
    {%- elif cookiecutter.rest_framework == 'DNRF' %}
    url = reverse("api-1.0.0:openapi-view")
    {%- endif %}
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_swagger_ui_not_accessible_by_normal_user(client):
    {%- if cookiecutter.rest_framework == 'DRF' %}
    url = reverse("api-docs")
    expected_status_code = 403
    {%- elif cookiecutter.rest_framework == 'DNRF' %}
    url = reverse("api-1.0.0:openapi-view")
    expected_status_code = HTTPStatus.FOUND
    {%- endif %}
    response = client.get(url)
    assert response.status_code == expected_status_code


def test_api_schema_generated_successfully(admin_client):
    {%- if cookiecutter.rest_framework == 'DRF' %}
    url = reverse("api-schema")
    {%- elif cookiecutter.rest_framework == 'DNRF' %}
    url = reverse("api-1.0.0:openapi-json")
    {%- endif %}
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK
