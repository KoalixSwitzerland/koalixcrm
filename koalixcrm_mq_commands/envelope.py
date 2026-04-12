import json
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class CommandEnvelope:
    """
    Generic command envelope with type and payload.
    """
    type: str
    payload: Dict[str, Any]

    def to_json(self) -> str:
        return json.dumps({
            "type": self.type,
            "payload": self.payload,
        })

    @staticmethod
    def from_json(data: str | Dict[str, Any]) -> "CommandEnvelope":
        obj = json.loads(data) if isinstance(data, str) else data
        return CommandEnvelope(type=obj.get("type"), payload=obj.get("payload", {}))
