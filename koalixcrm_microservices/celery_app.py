import os
import threading
import logging

import boto3
from celery import Celery
from celery.signals import worker_ready, task_unknown

# SQS broker URL format: sqs://aws_access_key_id:aws_secret_access_key@
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

app = Celery('koalixcrm', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
app.conf.timezone = 'UTC'
app.conf.task_default_queue = os.getenv('CELERY_SQS')

app.conf.task_reject_on_worker_lost = False
app.conf.task_acks_late = False

queue_name = os.getenv('CELERY_SQS')
region = os.getenv('AWS_REGION')

SQS_ENDPOINT_URL = os.getenv('SQS_ENDPOINT_URL')

if SQS_ENDPOINT_URL:
    account_id = '000000000000'
    app.conf.broker_transport_options = {
        'region': region or 'us-east-1',
        'is_secure': False,
        'polling_interval': 1,
        'visibility_timeout': 3600,
        'wait_time_seconds': 2,
        'predefined_queues': {
            queue_name: {
                'url': f'{SQS_ENDPOINT_URL}/{account_id}/{queue_name}'
            }
        } if queue_name else {},
        'queue_name_prefix': '',
    }
else:
    try:
        session = boto3.Session(profile_name=os.getenv('AWS_PROFILE'))
        sts = session.client('sts', region_name=region)
        account_id = sts.get_caller_identity()['Account']
    except Exception as e:
        logging.error(f"Failed to get AWS account ID: {e}")
        account_id = None

    app.conf.broker_transport_options = {
        'region': region,
        'polling_interval': 1,
        'visibility_timeout': 3600,
        'wait_time_seconds': 20,
        'predefined_queues': {
            queue_name: {
                'url': f'https://sqs.{region}.amazonaws.com/{account_id}/{queue_name}'
            }
        } if account_id else {},
        'queue_name_prefix': '',
    }

# Task modules to import. Empty for now — PDF export moved to the Java
# pdf-export-service which polls its own SQS queue. Future Python-side
# Celery tasks should be listed here.
app.conf.imports = []


def _float_env(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except Exception:
        return default


# Beat schedule intentionally empty after the PDF worker moved to Java.
app.conf.beat_schedule = {}

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))


@task_unknown.connect
def _on_task_unknown(name=None, task_id=None, message=None, exc=None, **kwargs):
    logger.warning(f"Received unregistered task '{name}' (ID: {task_id}). Acknowledging and discarding.")


@worker_ready.connect
def _on_worker_ready(sender=None, **kwargs):
    enable_poller = os.getenv('ENABLE_SQS_POLLER', 'true').lower() == 'true'
    if not enable_poller:
        logger.info('SQS poller disabled via ENABLE_SQS_POLLER=false')
        return
    try:
        from koalixcrm_microservices.sqs_poller import start_poller
    except Exception as e:
        logger.error(f"Failed importing SQS poller: {e}")
        return

    t = threading.Thread(target=start_poller, name='SQS-Poller', daemon=True)
    t.start()
    logger.info('Started SQS Poller background thread')
