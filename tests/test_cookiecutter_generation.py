import glob
import os
import re
import sys

import pytest

try:
    import sh
except ImportError:
    sh = None  # sh doesn't support Windows
from binaryornot.check import is_binary
from cookiecutter.exceptions import FailedHookException

PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)

if sys.platform.startswith("win"):
    pytest.skip("sh doesn't support windows", allow_module_level=True)
elif sys.platform.startswith("darwin") and os.getenv("CI"):
    pytest.skip("skipping slow macOS tests on CI", allow_module_level=True)

# Run auto-fixable styles checks - skipped on CI by default. These can be fixed
# automatically by running pre-commit after generation however they are tedious
# to fix in the template, so we don't insist too much in fixing them.
AUTOFIXABLE_STYLES = os.getenv("AUTOFIXABLE_STYLES") == "1"
auto_fixable = pytest.mark.skipif(not AUTOFIXABLE_STYLES, reason="auto-fixable")


@pytest.fixture
def context():
    return {
        "project_name": "My Test Project",
        "project_slug": "my_test_project",
        "author_name": "Test Author",
        "email": "test@example.com",
        "description": "A short description of the project.",
        "domain_name": "example.com",
    }


SUPPORTED_COMBINATIONS = [
    {"postgresql_version": "15"},
    {"postgresql_version": "14"},
    {"postgresql_version": "13"},
    {"postgresql_version": "12"},
    {"postgresql_version": "11"},
    {"postgresql_version": "10"},
    {"cloud_provider": "AWS", "use_whitenoise": "y"},
    {"cloud_provider": "AWS", "use_whitenoise": "n"},
    {"cloud_provider": "GCP", "use_whitenoise": "y"},
    {"cloud_provider": "GCP", "use_whitenoise": "n"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "Mailgun"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "Mailjet"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "Mandrill"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "Postmark"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "Sendgrid"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "SendinBlue"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "SparkPost"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "Other SMTP"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "None"},
    # Note: cloud_provider=None AND use_whitenoise=n is not supported
    {"cloud_provider": "AWS", "mail_service": "Mailgun"},
    {"cloud_provider": "AWS", "mail_service": "Amazon SES"},
    {"cloud_provider": "AWS", "mail_service": "Mailjet"},
    {"cloud_provider": "AWS", "mail_service": "Mandrill"},
    {"cloud_provider": "AWS", "mail_service": "Postmark"},
    {"cloud_provider": "AWS", "mail_service": "Sendgrid"},
    {"cloud_provider": "AWS", "mail_service": "SendinBlue"},
    {"cloud_provider": "AWS", "mail_service": "SparkPost"},
    {"cloud_provider": "AWS", "mail_service": "Other SMTP"},
    {"cloud_provider": "AWS", "mail_service": "None"},
    {"cloud_provider": "GCP", "mail_service": "Mailgun"},
    {"cloud_provider": "GCP", "mail_service": "Mailjet"},
    {"cloud_provider": "GCP", "mail_service": "Mandrill"},
    {"cloud_provider": "GCP", "mail_service": "Postmark"},
    {"cloud_provider": "GCP", "mail_service": "Sendgrid"},
    {"cloud_provider": "GCP", "mail_service": "SendinBlue"},
    {"cloud_provider": "GCP", "mail_service": "SparkPost"},
    {"cloud_provider": "GCP", "mail_service": "Other SMTP"},
    {"cloud_provider": "GCP", "mail_service": "None"},
    # Note: cloud_providers GCP and None
    # with mail_service Amazon SES is not supported
    {"use_whitenoise": "y"},
    {"use_whitenoise": "n"},
    {"use_mailpit": "y"},
    {"use_mailpit": "n"},
    {"use_sentry": "y"},
    {"use_sentry": "n"},
    {"rest_framework": "None"},
    {"rest_framework": "DRF"},
    {"rest_framework": "DNRF"},
    {"use_celery": "y"},
    {"use_celery": "n"},
]

UNSUPPORTED_COMBINATIONS = [
    {"cloud_provider": "None", "use_whitenoise": "n"},
    {"cloud_provider": "GCP", "mail_service": "Amazon SES"},
    {"cloud_provider": "None", "mail_service": "Amazon SES"},
    {"mail_service": "None", "use_mailpit": "y"},
]


def _fixture_id(ctx):
    """Helper to get a user-friendly test name from the parametrized context."""
    return "-".join(f"{key}:{value}" for key, value in ctx.items())


def build_files_list(base_dir):
    """Build a list containing absolute paths to the generated files."""
    return [os.path.join(dirpath, file_path) for dirpath, subdirs, files in os.walk(base_dir) for file_path in files]


def check_paths(paths):
    """Method to check all paths have correct substitutions."""
    # Assert that no match is found in any of the files
    for path in paths:
        if is_binary(path):
            continue

        for line in open(path):
            match = RE_OBJ.search(line)
            assert match is None, f"cookiecutter variable not replaced in {path}"


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_project_generation(cookies, context, context_override):
    """Test that project is generated and fully rendered."""

    result = cookies.bake(extra_context={**context, **context_override})
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == context["project_slug"]
    assert result.project_path.is_dir()

    paths = build_files_list(str(result.project_path))
    assert paths
    check_paths(paths)


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_flake8_passes(cookies, context_override):
    """Generated project should pass flake8."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.flake8(_cwd=str(result.project_path))
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@auto_fixable
@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_black_passes(cookies, context_override):
    """Check whether generated project passes black style."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.black(
            "--check",
            "--diff",
            "--exclude",
            "migrations",
            ".",
            _cwd=str(result.project_path),
        )
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@auto_fixable
@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_isort_passes(cookies, context_override):
    """Check whether generated project passes isort style."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.isort(_cwd=str(result.project_path))
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@auto_fixable
@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_django_upgrade_passes(cookies, context_override):
    """Check whether generated project passes django-upgrade."""
    result = cookies.bake(extra_context=context_override)

    python_files = [
        file_path.removeprefix(f"{result.project_path}/")
        for file_path in glob.glob(str(result.project_path / "**" / "*.py"), recursive=True)
    ]
    try:
        sh.django_upgrade(
            "--target-version",
            "4.2",
            *python_files,
            _cwd=str(result.project_path),
        )
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_djlint_lint_passes(cookies, context_override):
    """Check whether generated project passes djLint --lint."""
    result = cookies.bake(extra_context=context_override)

    autofixable_rules = "H014,T001"
    # TODO: remove T002 when fixed https://github.com/Riverside-Healthcare/djLint/issues/687
    ignored_rules = "H006,H030,H031,T002"
    try:
        sh.djlint("--lint", "--ignore", f"{autofixable_rules},{ignored_rules}", ".", _cwd=str(result.project_path))
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@auto_fixable
@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_djlint_check_passes(cookies, context_override):
    """Check whether generated project passes djLint --check."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.djlint("--check", ".", _cwd=str(result.project_path))
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@pytest.mark.parametrize("slug", ["project slug", "Project_Slug"])
def test_invalid_slug(cookies, context, slug):
    """Invalid slug should fail pre-generation hook."""
    context.update({"project_slug": slug})

    result = cookies.bake(extra_context=context)

    assert result.exit_code != 0
    assert isinstance(result.exception, FailedHookException)


@pytest.mark.parametrize("invalid_context", UNSUPPORTED_COMBINATIONS)
def test_error_if_incompatible(cookies, context, invalid_context):
    """It should not generate project an incompatible combination is selected."""
    context.update(invalid_context)
    result = cookies.bake(extra_context=context)

    assert result.exit_code != 0
    assert isinstance(result.exception, FailedHookException)


def test_trim_domain_email(cookies, context):
    """Check that leading and trailing spaces are trimmed in domain and email."""
    context.update(
        {
            "domain_name": "   example.com   ",
            "email": "  me@example.com  ",
        }
    )
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0

    prod_django_env = result.project_path / ".envs" / ".production" / ".django"
    assert "DJANGO_ALLOWED_HOSTS=.example.com" in prod_django_env.read_text()

    base_settings = result.project_path / "config" / "settings" / "base.py"
    assert '"me@example.com"' in base_settings.read_text()
