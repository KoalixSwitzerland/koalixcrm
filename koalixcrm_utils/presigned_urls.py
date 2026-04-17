"""
Helpers to generate short-lived presigned S3 URLs for template assets.

Used by the Django `/api/document-templates/{id}/{xsl,fop-config,logo}/`
endpoints to hand out time-limited download URLs that the Java PDF worker
then follows via HTTP 302.
"""
import os
from urllib.parse import urlparse, urlunparse

from koalixcrm_utils.aws_clients import get_s3_client

DEFAULT_EXPIRES_IN = int(os.getenv("PRESIGNED_URL_EXPIRES_IN", "300"))


def presigned_get_url_for_field(field_file, expires_in=DEFAULT_EXPIRES_IN):
    """
    Return a presigned GET URL for a Django FileField (backed by S3Boto3Storage).

    When running against MinIO (S3_ENDPOINT_URL set) the URL host comes from
    the endpoint; when running against AWS it's the standard
    `https://{bucket}.s3.{region}.amazonaws.com/{key}` form.
    Caller is responsible for checking that `field_file` is non-empty.
    """
    storage = field_file.storage
    bucket = storage.bucket_name
    key = field_file.name
    if getattr(storage, "location", ""):
        key = f"{storage.location.rstrip('/')}/{key}"

    client = get_s3_client(use_presigned_config=not os.getenv("S3_ENDPOINT_URL"))
    url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )
    return url
