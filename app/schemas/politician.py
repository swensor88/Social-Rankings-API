from datetime import date

from pydantic import BaseModel, ConfigDict


class PoliticianBase(BaseModel):
    political_body_id: int
    name: str
    current_position: str
    start_date: date
    end_date: date | None = None


class PoliticianCreate(PoliticianBase):
    pass


class PoliticianUpdate(BaseModel):
    political_body_id: int | None = None
    name: str | None = None
    current_position: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class PoliticianRead(PoliticianBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
