"""Celery-side unit test — exercises koalixcrm_mq_commands.envelope.

Runs under the `unit-celery` profile which disables Django (-p no:django).
Kept deliberately outside tests/ so it does not overlap with the Django unit
suite nor with the integration suite.
"""
from koalixcrm_mq_commands.envelope import CommandEnvelope


def test_envelope_roundtrip():
    env = CommandEnvelope(type="pdf.export", payload={"invoice_id": 42})
    assert CommandEnvelope.from_json(env.to_json()) == env


def test_envelope_from_dict():
    env = CommandEnvelope.from_json({"type": "pdf.export", "payload": {"x": 1}})
    assert env.type == "pdf.export"
    assert env.payload == {"x": 1}


def test_envelope_missing_payload_defaults_empty():
    env = CommandEnvelope.from_json({"type": "noop"})
    assert env.payload == {}
