{% if cookiecutter.rest_framework == 'DRF' -%}
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
{% elif cookiecutter.rest_framework == 'DNRF' -%}
from django.contrib.admin.views.decorators import staff_member_required
from ninja import NinjaAPI

import orjson
from ninja.parser import Parser
from django.http import HttpRequest

{% endif %}

{%- if cookiecutter.rest_framework == 'DRF' %}
router = DefaultRouter() if settings.DEBUG else SimpleRouter()

urlpatterns = router.urls
app_name = "api"
{%- elif cookiecutter.rest_framework == 'DNRF' %}
class ORJSONParser(Parser):
    def parse_body(self, request: HttpRequest):
        return orjson.loads(request.body)


api = NinjaAPI(
    parser=ORJSONParser(),
    docs_decorator=staff_member_required,
    title="{{ cookiecutter.project_name }} API",
    description="Documentation of API endpoints of {{ cookiecutter.project_name }}",
    version="1.0.0",
)

# Your stuff: custom routers/api urls go here
{%- endif %}
