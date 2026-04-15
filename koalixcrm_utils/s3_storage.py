"""
S3-backed storage backend for template files and media.

Uses the same S3/MinIO connection settings as the rest of the project
(S3_ENDPOINT_URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).

Files are stored in the S3_TEMPLATE_BUCKET bucket (defaults to
koalixcrm-pdf-exports, under the 'templates/' prefix).
"""
import os

from storages.backends.s3boto3 import S3Boto3Storage


class TemplateFileStorage(S3Boto3Storage):
    """
    S3 storage for DocumentTemplate files (XSL, FOP config, logos).
    Uploaded via Django admin, downloaded by the Celery worker before FOP runs.
    """
    bucket_name = os.getenv("S3_PDF_BUCKET", "koalixcrm-pdf-exports")
    location = "templates"
    file_overwrite = False
    default_acl = None

    def __init__(self, **kwargs):
        endpoint_url = os.getenv("S3_ENDPOINT_URL")
        if endpoint_url:
            kwargs.setdefault("endpoint_url", endpoint_url)
            kwargs.setdefault("access_key", os.getenv("AWS_ACCESS_KEY_ID", "minioadmin"))
            kwargs.setdefault("secret_key", os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin123"))
            kwargs.setdefault("custom_domain", None)
            # MinIO needs path-style addressing
            kwargs.setdefault("addressing_style", "path")
        kwargs.setdefault("region_name", os.getenv("AWS_REGION", "eu-west-3"))
        super().__init__(**kwargs)
