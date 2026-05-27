from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PoliticalBody(Base):
    __tablename__ = "political_body"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    politicians = relationship("Politician", back_populates="political_body", cascade="all, delete")
