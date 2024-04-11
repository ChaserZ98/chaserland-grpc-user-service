from __future__ import annotations

from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, func, text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
from .schemas import Scope


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("NOW()"),
        onupdate=text("NOW()"),
    )
    deleted_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )


class IdMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class UUIDMixin:
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )


class User(Base, TimestampMixin, UUIDMixin):
    __tablename__ = "users"

    scopes: Mapped[list[Scope]] = mapped_column(
        MutableList.as_mutable(ARRAY(String)), default=[], nullable=False
    )
    local_auth: Mapped[LocalAuth] = relationship(
        "LocalAuth", back_populates="user", lazy="selectin"
    )
    oauths: Mapped[list[OAuth]] = relationship(
        "OAuth", back_populates="user", lazy="selectin"
    )


class LocalAuth(Base, TimestampMixin, IdMixin):
    __tablename__ = "local_auths"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    username: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped[User] = relationship(
        "User", back_populates="local_auth", lazy="selectin"
    )


class OAuth(Base, TimestampMixin, IdMixin):
    __tablename__ = "oauths"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )
    oauth_name: Mapped[str] = mapped_column(String, nullable=False)
    oauth_id: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True
    )
    oauth_token_type: Mapped[str] = mapped_column(String, nullable=False)
    oauth_access_token: Mapped[str] = mapped_column(String, nullable=False)
    oauth_refresh_token: Mapped[str] = mapped_column(String, nullable=True)
    oauth_issue_at: Mapped[int] = mapped_column(Integer, nullable=False)
    oauth_expires_at: Mapped[int] = mapped_column(Integer, nullable=True)
    oauth_scope: Mapped[str] = mapped_column(String, nullable=True)

    user: Mapped[User] = relationship("User", back_populates="oauths", lazy="selectin")
