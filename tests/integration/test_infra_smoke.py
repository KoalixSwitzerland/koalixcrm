"""Integration smoke test — exercises both Django and Celery side components
against the live infrastructure (MinIO for S3, ElasticMQ for SQS) brought up
by /app/koalixcrm_system/docker-compose.yml under the `integration` profile.

Runs only when -m integration is selected. Kept outside the Django unit suite
(which excludes `integration`) and outside the Celery unit suite (which only
scans koalixcrm_microservices/).
"""
import os
import uuid

import boto3
import pytest

from koalixcrm_mq_commands.envelope import CommandEnvelope


pytestmark = pytest.mark.integration


@pytest.fixture
def s3_client():
    endpoint = os.environ["S3_ENDPOINT_URL"]
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "minioadmin"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "minioadmin123"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )


@pytest.fixture
def sqs_client():
    endpoint = os.environ["SQS_ENDPOINT_URL"]
    return boto3.client(
        "sqs",
        endpoint_url=endpoint,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "dummy"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "dummy"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )


def test_minio_roundtrip_on_pdf_bucket(s3_client):
    bucket = os.environ.get("S3_PDF_BUCKET", "koalixcrm-pdf-exports")
    key = f"integration-test-{uuid.uuid4()}.txt"
    body = b"hello from integration test"

    s3_client.put_object(Bucket=bucket, Key=key, Body=body)
    got = s3_client.get_object(Bucket=bucket, Key=key)["Body"].read()
    s3_client.delete_object(Bucket=bucket, Key=key)

    assert got == body


def test_elasticmq_envelope_roundtrip(sqs_client):
    """Send a CommandEnvelope through the MQ the Celery worker would read from."""
    queue_name = os.environ.get("CELERY_SQS", "koalixcrm-celery-sqs")
    q = sqs_client.create_queue(QueueName=queue_name)
    url = q["QueueUrl"]

    env = CommandEnvelope(type="pdf.export", payload={"invoice_id": 1})
    sqs_client.send_message(QueueUrl=url, MessageBody=env.to_json())

    msgs = sqs_client.receive_message(QueueUrl=url, WaitTimeSeconds=2, MaxNumberOfMessages=1)
    received = msgs.get("Messages", [])
    assert received, "expected at least one message on the celery queue"
    got = CommandEnvelope.from_json(received[0]["Body"])
    assert got == env

    sqs_client.delete_message(QueueUrl=url, ReceiptHandle=received[0]["ReceiptHandle"])


def test_django_backend_reachable():
    """Django is up and admin endpoint responds (basic cross-component check)."""
    import time
    import urllib.request
    import urllib.error

    url = "http://backend:8000/admin/login/"
    last_err: Exception | None = None
    for _ in range(30):
        try:
            with urllib.request.urlopen(url, timeout=5) as r:
                assert r.status == 200
                return
        except (urllib.error.URLError, ConnectionError) as exc:
            last_err = exc
            time.sleep(2)
    raise AssertionError(f"backend never became ready: {last_err!r}")
