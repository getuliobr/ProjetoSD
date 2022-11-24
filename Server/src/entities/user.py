
from pydantic import BaseModel


class User(BaseModel):
    ip: str
    time_from_last_tile: float