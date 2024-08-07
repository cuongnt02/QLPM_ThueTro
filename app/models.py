from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, WriteOnlyMapped
from sqlalchemy.orm import mapped_column, relationship
from app import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(150), index=True, unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))
    full_name: Mapped[str] = mapped_column(String(75))
    phone_number: Mapped[Optional[str]] = mapped_column(String(12))
    address: Mapped[Optional[str]] = mapped_column(String(200))
    posts: WriteOnlyMapped['Post'] = relationship(back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(
        index=True,
        default=lambda: datetime.now(tz=ZoneInfo("Asia/Ho_Chi_Minh")))
    user_id: Mapped[str] = mapped_column(ForeignKey(User.id))

    author: Mapped[User] = relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.title)
