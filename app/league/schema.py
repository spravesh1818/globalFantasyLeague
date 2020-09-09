from pydantic import BaseModel


class League(BaseModel):
    name: str
    division: str
