{% if cookiecutter.rest_framework == 'DRF' -%}
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
{% elif cookiecutter.rest_framework == 'DNRF' -%}
import orjson
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.parser import Parser

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
