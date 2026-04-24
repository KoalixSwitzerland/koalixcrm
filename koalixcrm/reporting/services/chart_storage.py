# -*- coding: utf-8 -*-
"""S3-backed storage for project-report charts.

The legacy synchronous flow wrote ``project_costs_overview.svg`` into
``settings.PDF_OUTPUT_ROOT`` and inlined the local path into the XML so
the in-process FOP could pick it up via the filesystem. The async flow
runs FOP in a separate Java service on a different host: it cannot read
local files, so we upload the chart to the same MinIO/S3 bucket as PDF
exports and ship a presigned GET URL via JSON.

The Java orchestrator downloads the URL into the FOP working directory
and rewrites the ``project_cost_overview`` element to the local filename
before invoking FOP. (FOP can technically follow ``http(s)://`` URLs in
``<fo:external-graphic>``, but bearer-token auth and presigned URL TTLs
make that fragile — keeping the rewrite in the orchestrator is simpler.)
"""
import io
import os
import uuid

import matplotlib
matplotlib.use('Agg')  # headless backend for worker / API processes
import matplotlib.dates as mdates  # noqa: E402
from matplotlib import pyplot  # noqa: E402
import pandas  # noqa: E402

from koalixcrm_utils.aws_clients import get_s3_client


CHART_KEY_PREFIX = os.getenv("S3_REPORT_CHART_PREFIX", "report-charts")
PRESIGNED_URL_EXPIRES_IN = int(os.getenv("PRESIGNED_URL_EXPIRES_IN", "300"))


def _bucket():
    return os.getenv("S3_PDF_BUCKET", "koalixcrm-pdf-exports")


def build_project_cost_overview_svg_bytes(project) -> bytes:
    """Produce the same SVG the legacy ``Project.create_project_cost_overview_illustration``
    wrote to disk, but as in-memory bytes. No filesystem I/O.
    """
    from koalixcrm.reporting.models.reporting_period import ReportingPeriod

    accumulated_effective_costs = {}
    accumulated_effective_cost = 0
    reporting_periods = list(
        ReportingPeriod.objects.filter(project=project.id).order_by('begin')
    )
    for rp in reporting_periods:
        accumulated_effective_cost += project.effective_costs(reporting_period=rp)
        accumulated_effective_costs[rp] = accumulated_effective_cost

    # The original function shadowed `reporting_period` inside the loop and
    # then passed the loop's last value into `planned_costs_in_buckets`.
    # Mirror that behaviour so output is identical.
    last_reporting_period = reporting_periods[-1] if reporting_periods else None
    accumulated_planned_costs = project.planned_costs_in_buckets(
        reporting_period=last_reporting_period, buckets=reporting_periods
    )

    data_frame = None
    for rp in reporting_periods:
        if rp.status and rp.status.is_done:
            confirmed = int(accumulated_effective_costs[rp])
            not_confirmed = int(accumulated_effective_costs[rp])
        else:
            confirmed = None
            not_confirmed = int(accumulated_effective_costs[rp])
        if data_frame is None:
            data_frame = pandas.DataFrame(
                [[rp.begin, None, 0, 0, 0],
                 [rp.end, None, int(accumulated_planned_costs[rp]), confirmed, not_confirmed]],
                columns=('x', 'Budget', 'Estimation',
                         'Effective confirmed', 'Effective not confirmed'),
            )
        else:
            row = pandas.DataFrame(
                [[rp.end, None, int(accumulated_planned_costs[rp]), confirmed, not_confirmed]],
                columns=('x', 'Budget', 'Estimation',
                         'Effective confirmed', 'Effective not confirmed'),
            )
            data_frame = pandas.concat([data_frame, row], ignore_index=False)

    # `seaborn-darkgrid` is gone in newer matplotlib; fall back gracefully.
    try:
        pyplot.style.use('seaborn-darkgrid')
    except (OSError, ValueError):
        pyplot.style.use('seaborn-v0_8-darkgrid')

    figure, axis = pyplot.subplots()
    if data_frame is not None:
        axis.plot(data_frame['x'], data_frame.get('Budget'),
                  marker=' ', color='red', linewidth=1, alpha=0.9, label='Agreed Budget')
        axis.plot(data_frame['x'], data_frame.get('Estimation'),
                  marker='o', color='orangered', linewidth=2, alpha=0.5, label='Estimation (accumulated)')
        axis.plot(data_frame['x'], data_frame.get('Effective confirmed'),
                  marker='o', color='orange', linewidth=2, alpha=0.5,
                  label='Effective confirmed (accumulated)')
        axis.plot(data_frame['x'], data_frame.get('Effective not confirmed'),
                  marker='o', color='gold', linewidth=2, alpha=0.5,
                  label='Effective not confirmed (accumulated)')
    axis.legend(loc=2, ncol=1)
    figure.autofmt_xdate()
    axis.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    axis.set_title('Project Costs Overview', loc='left', fontsize=12, fontweight=0, color='orange')
    axis.set_xlabel('Date')
    axis.set_ylabel('Costs in ' + str(project.default_currency))

    buf = io.BytesIO()
    figure.savefig(buf, format='svg')
    figure.clf()
    pyplot.close(figure)
    return buf.getvalue()


def upload_project_cost_overview_svg(project) -> str:
    """Render + upload the SVG, return a presigned GET URL the Java
    orchestrator can fetch without bearer auth.
    """
    svg = build_project_cost_overview_svg_bytes(project)
    key = f"{CHART_KEY_PREFIX}/project_{project.id}_{uuid.uuid4().hex}.svg"
    bucket = _bucket()

    client = get_s3_client(use_presigned_config=not os.getenv("S3_ENDPOINT_URL"))
    client.put_object(
        Bucket=bucket,
        Key=key,
        Body=svg,
        ContentType='image/svg+xml',
    )
    return client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=PRESIGNED_URL_EXPIRES_IN,
    )
