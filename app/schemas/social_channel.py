from pydantic import BaseModel, ConfigDict

from app.models.enums import DownloadFrequency, DownloadType


class SocialChannelBase(BaseModel):
    name: str
    audience_type: str
    download_type: DownloadType
    download_frequency: DownloadFrequency


class SocialChannelCreate(SocialChannelBase):
    pass


class SocialChannelUpdate(BaseModel):
    name: str | None = None
    audience_type: str | None = None
    download_type: DownloadType | None = None
    download_frequency: DownloadFrequency | None = None


class SocialChannelRead(SocialChannelBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
