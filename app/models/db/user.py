from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=False)
    hashed_password: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"
