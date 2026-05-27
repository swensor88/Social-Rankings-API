from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    politician_id: Mapped[int] = mapped_column(ForeignKey("politicians.id"), nullable=False)
    social_channel_id: Mapped[int] = mapped_column(ForeignKey("social_channel.id"), nullable=False)
    total_audience: Mapped[int] = mapped_column(Integer, nullable=False)

    politician = relationship("Politician", back_populates="accounts")
    social_channel = relationship("SocialChannel", back_populates="accounts")
