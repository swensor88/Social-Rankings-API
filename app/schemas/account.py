from pydantic import BaseModel, ConfigDict


class AccountBase(BaseModel):
    politician_id: int
    social_channel_id: int
    total_audience: int


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    politician_id: int | None = None
    social_channel_id: int | None = None
    total_audience: int | None = None


class AccountRead(AccountBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
