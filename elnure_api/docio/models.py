from dataclasses import dataclass
from typing import Any


@dataclass
class Sheet:
    name: str
    data: Any
