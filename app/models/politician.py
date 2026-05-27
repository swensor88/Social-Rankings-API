from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Politician(Base):
    __tablename__ = "politicians"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    political_body_id: Mapped[int] = mapped_column(ForeignKey("political_body.id"), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    current_position: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    political_body = relationship("PoliticalBody", back_populates="politicians")
    accounts = relationship("Account", back_populates="politician", cascade="all, delete")
