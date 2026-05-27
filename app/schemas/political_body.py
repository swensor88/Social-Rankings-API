from pydantic import BaseModel, ConfigDict


class PoliticalBodyBase(BaseModel):
    name: str
    description: str


class PoliticalBodyCreate(PoliticalBodyBase):
    pass


class PoliticalBodyUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class PoliticalBodyRead(PoliticalBodyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
