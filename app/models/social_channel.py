from sqlalchemy import Enum, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import DownloadFrequency, DownloadType


class SocialChannel(Base):
    __tablename__ = "social_channel"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    audience_type: Mapped[str] = mapped_column(Text, nullable=False)
    download_type: Mapped[DownloadType] = mapped_column(
        Enum(DownloadType, name="download_type_enum"), nullable=False
    )
    download_frequency: Mapped[DownloadFrequency] = mapped_column(
        Enum(DownloadFrequency, name="download_frequency_enum"), nullable=False
    )

    accounts = relationship("Account", back_populates="social_channel", cascade="all, delete")
