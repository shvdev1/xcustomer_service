from pydantic import BaseModel


class Customer(BaseModel):
    id: int | None = None
    name: str
