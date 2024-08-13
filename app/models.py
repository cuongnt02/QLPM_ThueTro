from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional
from sqlalchemy import String, Text, ForeignKey, Enum, Integer, Float
from sqlalchemy.orm import Mapped, WriteOnlyMapped
from sqlalchemy.orm import mapped_column, relationship
from flask_login import UserMixin
from app import login
from enum import Enum as RoleEnum
from app import db


class UserRole(RoleEnum):
    USER = 1
    ADMIN = 2
    LANDLORD = 3


@login.user_loader
def load_user(id):
    return db.session.get(User, id)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(150), index=True, unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))
    full_name: Mapped[str] = mapped_column(String(75))
    phone_number: Mapped[Optional[str]] = mapped_column(String(12))
    address: Mapped[Optional[str]] = mapped_column(String(200))
    avatar: Mapped[Optional[str]] = mapped_column(String(256))
    user_role: Mapped[UserRole] = mapped_column(Enum(UserRole),
                                                default=UserRole.USER)

    posts: WriteOnlyMapped['Post'] = relationship(back_populates='author')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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


class Motel(db.Model):
    __tablename__ = "motels"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    address: Mapped[str] = mapped_column(String(200))
    max_room: Mapped[int] = mapped_column(Integer)


class Room(db.Model):
    __tablename__ = "rooms"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    room_name: Mapped[str] = mapped_column(String(100))
    base_price: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(Text)
    water_price: Mapped[float] = mapped_column(Float)
    electric_price: Mapped[float] = mapped_column(Float)
    picture: Mapped[str] = mapped_column(String(256))
