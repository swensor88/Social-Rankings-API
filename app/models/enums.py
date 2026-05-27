import enum


class DownloadType(str, enum.Enum):
    API = "api"
    WEB = "web"
    S3 = "s3"


class DownloadFrequency(str, enum.Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
