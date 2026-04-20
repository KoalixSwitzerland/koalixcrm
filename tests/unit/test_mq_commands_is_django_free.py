# -*- coding: utf-8 -*-
"""CR-3: ``koalixcrm_mq_commands`` must stay dataclass-only.

WFS copies this package verbatim to publish the same SQS payload to the
Java FOP worker. A leaked ``django.*`` import would either drag the whole
Django app along or fail to load without ``DJANGO_SETTINGS_MODULE``.

The test isolates the import in a subprocess so it runs without Django
configured — any ``import django`` chain surfaces as a ``ModuleNotFoundError``
or shows up in ``sys.modules``.
"""
import subprocess
import sys
import textwrap


SCRIPT = textwrap.dedent(
    """
    import os, sys
    # Guarantee Django isn't auto-configured by the harness.
    os.environ.pop('DJANGO_SETTINGS_MODULE', None)

    import koalixcrm_mq_commands  # noqa: F401

    leaked = sorted(m for m in sys.modules if m == 'django' or m.startswith('django.'))
    if leaked:
        print('LEAKED:' + ','.join(leaked))
        sys.exit(1)
    print('OK')
    """
).strip()


def test_mq_commands_does_not_import_django():
    result = subprocess.run(
        [sys.executable, '-c', SCRIPT],
        capture_output=True,
        text=True,
        # Run without inheriting DJANGO_SETTINGS_MODULE from the pytest env.
        env={'PATH': '/usr/bin:/bin:/usr/local/bin'},
    )
    assert result.returncode == 0, (
        f"koalixcrm_mq_commands pulls Django into sys.modules.\n"
        f"stdout: {result.stdout!r}\nstderr: {result.stderr!r}"
    )
    assert result.stdout.strip() == 'OK'
