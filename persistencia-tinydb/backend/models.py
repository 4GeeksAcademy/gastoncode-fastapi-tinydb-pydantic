from pydantic import BaseModel, ConfigDict


class ContactCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    email: str
    age: int
    city: str


class ContactUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    email: str | None = None
    age: int | None = None
    city: str | None = None