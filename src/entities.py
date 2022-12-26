import json
from datetime import datetime
from typing import Optional

from dataclasses import dataclass


@dataclass
class Message:
    site: str
    checked_at: datetime
    up: Optional[bool] = None
    downtime_reason: Optional[str] = None

    def to_jsonb(self) -> bytes:
        return json.dumps(
            {
                "site": self.site,
                "up": self.up,
                "downtime_reason": self.downtime_reason,
                "checked_at": self.checked_at.isoformat(),
            }
        ).encode("utf-8")

    @staticmethod
    def from_jsonb(json_string_bytes: bytes) -> "Message":
        message_dict = json.loads(json_string_bytes.decode("utf-8"))
        return Message(
            checked_at=datetime.fromisoformat(message_dict.pop("checked_at")),
            **message_dict
        )


@dataclass
class PeriodicCheckerInput:
    site: str
    regexp: Optional[str] = None
    status_code: Optional[int] = 200
    period: Optional[int] = 10


@dataclass
class CheckResult:
    up: bool
    downtime_reason: Optional[str] = None
