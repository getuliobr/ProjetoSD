
from typing import Optional

from pydantic import BaseModel
from pydantic.color import Color


class Tile(BaseModel):
    x: int
    y: int
    color: Color
    ip: Optional[str]