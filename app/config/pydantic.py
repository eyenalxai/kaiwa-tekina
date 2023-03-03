from pydantic import BaseModel


class Immutable(BaseModel):
    class Config:
        frozen = True
