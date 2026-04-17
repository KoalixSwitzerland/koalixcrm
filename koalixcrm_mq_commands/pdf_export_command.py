from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class PDFExportCommand:
    """
    Command to trigger PDF generation for a sales document or reporting object.

    Fields:
    - process_id: int (id of PDFExportProcess)
    - source_model: str (e.g. 'Invoice', 'Quote', 'DeliveryNote')
    - source_id: int (id of the source object)
    - template_set_id: int (id of the DocumentTemplate)
    - printed_by_user_id: int (id of the User who triggered the export)
    """

    process_id: int
    source_model: str
    source_id: int
    template_set_id: int
    printed_by_user_id: int

    TYPE: str = "PDFExportCommand"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.TYPE,
            "payload": {
                "process_id": self.process_id,
                "source_model": self.source_model,
                "source_id": self.source_id,
                "template_set_id": self.template_set_id,
                "printed_by_user_id": self.printed_by_user_id,
            },
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PDFExportCommand:
        if "type" in data:
            if data.get("type") != cls.TYPE:
                raise ValueError(f"Invalid command type: {data.get('type')}")
            p = data.get("payload", {})
        else:
            p = data

        return cls(
            process_id=int(p["process_id"]),
            source_model=str(p["source_model"]),
            source_id=int(p["source_id"]),
            template_set_id=int(p["template_set_id"]),
            printed_by_user_id=int(p["printed_by_user_id"]),
        )

    @classmethod
    def from_json(cls, s: str) -> PDFExportCommand:
        return cls.from_dict(json.loads(s))
