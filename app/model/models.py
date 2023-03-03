from datetime import datetime

from sqlalchemy import BIGINT, TIMESTAMP, Boolean
from sqlalchemy import Enum as EnumType
from sqlalchemy import ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.model.schema.open_ai import Role


class Base(DeclarativeBase):
    # WPS420 Found wrong keyword: pass
    # WPS604 Found incorrect node inside `class` body
    pass  # noqa: WPS420, WPS604


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003, VNE003
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )

    telegram_id: Mapped[int] = mapped_column(BIGINT, unique=True)

    username: Mapped[str | None] = mapped_column(
        String(32),  # noqa: WPS432 Found magic number
    )
    full_name: Mapped[str | None] = mapped_column(
        String(128),  # noqa: WPS432 Found magic number
    )

    messages: Mapped[list["MessageModel"]] = relationship(back_populates="user")

    is_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    tokens_used: Mapped[int] = mapped_column(Integer(), default=0)


class MessageModel(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003, VNE003
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )

    # WPS432 Found magic number: 4096
    content: Mapped[str] = mapped_column(String(4096))  # noqa: WPS432
    role: Mapped[Role] = mapped_column(EnumType(Role, name="role"))

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserModel"] = relationship(back_populates="messages")