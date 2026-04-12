"""
Centralized boto3 client factory with local-service endpoint support.

When S3_ENDPOINT_URL or SQS_ENDPOINT_URL environment variables are set,
boto3 clients are configured to use local alternatives (MinIO, ElasticMQ)
instead of real AWS services. When unset, clients use standard AWS endpoints.
"""
import os
import logging

import boto3
from botocore.config import Config

logger = logging.getLogger(__name__)

S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
SQS_ENDPOINT_URL = os.getenv("SQS_ENDPOINT_URL")


def get_s3_client(region_name=None, use_presigned_config=False):
    """
    Return a boto3 S3 client, pointing to MinIO when S3_ENDPOINT_URL is set.
    """
    region = region_name or os.getenv("AWS_REGION", "eu-west-3")
    kwargs = {"region_name": region}

    if S3_ENDPOINT_URL:
        kwargs["endpoint_url"] = S3_ENDPOINT_URL
        kwargs["config"] = Config(
            signature_version="s3v4",
            s3={"addressing_style": "path"},
        )
        kwargs["aws_access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
        kwargs["aws_secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin123")
    elif use_presigned_config:
        kwargs["config"] = Config(
            signature_version="s3v4",
            s3={"addressing_style": "virtual"},
        )

    return boto3.client("s3", **kwargs)


def get_sqs_client(region_name=None):
    """
    Return a boto3 SQS low-level client, pointing to ElasticMQ when SQS_ENDPOINT_URL is set.
    """
    region = region_name or os.getenv("AWS_REGION", "eu-west-3")
    kwargs = {"region_name": region}

    if SQS_ENDPOINT_URL:
        kwargs["endpoint_url"] = SQS_ENDPOINT_URL
        kwargs["aws_access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID", "dummy")
        kwargs["aws_secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY", "dummy")

    return boto3.client("sqs", **kwargs)


def get_sqs_resource(region_name=None):
    """
    Return a boto3 SQS high-level resource, pointing to ElasticMQ when SQS_ENDPOINT_URL is set.
    """
    region = region_name or os.getenv("AWS_REGION", "eu-west-3")
    kwargs = {"region_name": region}

    if SQS_ENDPOINT_URL:
        kwargs["endpoint_url"] = SQS_ENDPOINT_URL
        kwargs["aws_access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID", "dummy")
        kwargs["aws_secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY", "dummy")

    return boto3.resource("sqs", **kwargs)


def get_sqs_queue(queue_name=None):
    """
    Convenience function returning a boto3 SQS queue by name.
    """
    q_name = queue_name or os.getenv("KOALIXCRM_MICROSERVICE_SQS", "koalixcrm-microservice-sqs")
    sqs = get_sqs_resource()
    return sqs.get_queue_by_name(QueueName=q_name)
