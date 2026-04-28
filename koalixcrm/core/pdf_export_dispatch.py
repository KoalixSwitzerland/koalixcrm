# -*- coding: utf-8 -*-
"""CR-4: swappable PDF-export dispatcher.

The default dispatcher sends `PDFExportCommand` to the koalixcrm SQS queue
via `koalixcrm_utils.aws_clients.get_sqs_queue`. Forks (e.g. WFS, which
already owns a broker/poller fleet) can override this by setting:

    KOALIXCRM_PDF_EXPORT_DISPATCHER = "my_fork.dispatchers.send_pdf_command"

The callable must accept a single `PDFExportCommand` argument and is
responsible for serialising and enqueuing it. It may raise on failure;
the caller handles logging + marking the process as failed.
"""
from __future__ import annotations

from typing import Callable

from django.conf import settings
from django.utils.module_loading import import_string

from koalixcrm_mq_commands import PDFExportCommand

_DEFAULT = "koalixcrm.core.pdf_export_dispatch.default_sqs_dispatcher"


def default_sqs_dispatcher(command: PDFExportCommand) -> None:
    """Send the command as JSON to the koalixcrm SQS queue."""
    from koalixcrm_utils.aws_clients import get_sqs_queue
    queue = get_sqs_queue()
    queue.send_message(MessageBody=command.to_json())


def get_dispatcher() -> Callable[[PDFExportCommand], None]:
    """Resolve the configured dispatcher at call time (not import time)."""
    dotted = getattr(settings, "KOALIXCRM_PDF_EXPORT_DISPATCHER", _DEFAULT)
    return import_string(dotted)
