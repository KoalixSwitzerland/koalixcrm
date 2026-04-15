import json
import logging
import os
import time
from typing import Any, Dict

from koalixcrm_utils.aws_clients import get_sqs_client
from koalixcrm_mq_commands import CommandEnvelope, PDFExportCommand
from koalixcrm_microservices.celery_app import app as celery_app

logger = logging.getLogger(__name__)


def _parse_message_body(body: str) -> Dict[str, Any]:
    try:
        data = json.loads(body)
        if isinstance(data, str):
            data = json.loads(data)
        return data
    except Exception:
        logger.warning("SQS message body could not be parsed as JSON; skipping")
        return {}


def dispatch_command(env: CommandEnvelope) -> bool:
    """
    Dispatch a CommandEnvelope to the appropriate Celery task.
    Returns True if the message was handled and can be deleted.
    """
    try:
        TASK_ROUTES = {
            PDFExportCommand.TYPE: [
                'koalixcrm_microservices.pdf_export_task.tasks.run',
            ],
        }

        routes = TASK_ROUTES.get(env.type)
        if routes:
            payload = env.payload
            for task_name in routes:
                try:
                    celery_app.send_task(task_name, args=[payload])
                except Exception:
                    logger.exception("Failed to queue task '%s' for command type=%s", task_name, env.type)
            return True

        logger.info("Unsupported command type received: %s", env.type)
        return True
    except Exception:
        logger.exception("Failed to dispatch command type=%s", env.type)
        return False


def start_poller():
    """
    Endless loop polling SQS every N seconds and dispatching commands to Celery.
    """
    queue_name = os.getenv("KOALIXCRM_MICROSERVICE_SQS")
    sleep_seconds = float(os.getenv("POLL_SLEEP_SECONDS", "2"))

    sqs = get_sqs_client()
    while True:
        try:
            try:
                queue_url = sqs.get_queue_url(QueueName=queue_name)["QueueUrl"]
            except Exception as e:
                logger.error("Cannot resolve SQS queue '%s': %s", queue_name, e)
                time.sleep(sleep_seconds)
                continue

            resp = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=5,
                WaitTimeSeconds=2,
                VisibilityTimeout=60,
            )
            messages = resp.get("Messages", [])
            if not messages:
                time.sleep(sleep_seconds)
                continue

            for m in messages:
                receipt = m.get("ReceiptHandle")
                body = m.get("Body", "")
                data = _parse_message_body(body)
                env = CommandEnvelope.from_json(data) if data else None

                handled = False
                if env:
                    handled = dispatch_command(env)
                else:
                    handled = True

                if handled and receipt:
                    try:
                        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt)
                    except Exception as de:
                        logger.warning("Failed to delete SQS message: %s", de)
        except Exception as outer:
            logger.exception("SQS poll error: %s", outer)
            time.sleep(sleep_seconds)
