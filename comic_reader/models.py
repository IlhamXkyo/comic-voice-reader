"""
Definisi Model Domain Inti untuk ComicVoice Reader
Menyediakan tipe data yang tervalidasi dan Single Source of Truth (SSOT).
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class ReadingZone:
    """Model data koordinat dan ukuran area bidik layar."""
    x: int
    y: int
    width: int
    height: int

    def to_dict(self) -> Dict[str, int]:
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height
        }

    @classmethod
    def from_dict(cls, data: Any, default_x: int = 350, default_y: int = 100,
                  default_w: int = 650, default_h: int = 850) -> "ReadingZone":
        if not isinstance(data, dict):
            return cls(default_x, default_y, default_w, default_h)
        return cls(
            x=int(data.get("x", default_x)),
            y=int(data.get("y", default_y)),
            width=max(50, int(data.get("width", default_w))),
            height=max(50, int(data.get("height", default_h)))
        )
