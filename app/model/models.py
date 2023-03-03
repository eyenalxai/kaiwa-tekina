from datetime import datetime

from sqlalchemy import func, TIMESTAMP, String, ForeignKey, Enum as EnumType
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from app.model.schema.open_ai import Role


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003, VNE003
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    telegram_id: Mapped[str] = mapped_column(String(512), unique=True)

    messages: Mapped[list["MessageModel"]] = relationship(back_populates="user")


class MessageModel(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003, VNE003
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    content: Mapped[str] = mapped_column(String(4096))
    role: Mapped[Role] = mapped_column(EnumType(Role, name="role"))

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserModel"] = relationship(back_populates="messages")
