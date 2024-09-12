# models.py

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional, List
from sqlalchemy import String, Text, ForeignKey, Enum, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4
from flask_login import UserMixin
from enum import Enum as RoleEnum
from app import db, login


# Enum for user roles
class UserRole(RoleEnum):
    USER = 1
    ADMIN = 2
    LANDLORD = 3


# User loader function for Flask-Login
@login.user_loader
def load_user(id):
    return db.session.get(User, id)


# User model
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36),
                                    primary_key=True, default=uuid4())
    username: Mapped[str] = mapped_column(String(50), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(150), index=True, unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))
    full_name: Mapped[str] = mapped_column(String(75))
    phone_number: Mapped[Optional[str]] = mapped_column(String(12))
    address: Mapped[Optional[str]] = mapped_column(String(200))
    avatar: Mapped[Optional[str]] = mapped_column(String(256))
    user_role: Mapped[UserRole] = mapped_column(Enum(UserRole, length=255),
                                                default=UserRole.USER)

    posts: Mapped[List['Post']] = relationship(back_populates='author')
    bookings: Mapped[List['Booking']] = relationship(back_populates='user')
    messages_sent: Mapped[List['Message']] = relationship(
        foreign_keys='Message.sender_id', back_populates='sender'
    )
    messages_received: Mapped[List['Message']] = relationship(
        foreign_keys='Message.receiver_id', back_populates='receiver'
    )
    reviews: Mapped[List['Review']] = relationship(back_populates='user')
    motels: Mapped[List['Motel']] = relationship(back_populates='user',
                                                 cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'




# Motel model
class Motel(db.Model):
    __tablename__ = "motels"

    id: Mapped[str] = mapped_column(String(36), primary_key=True,
                                    default=uuid4())
    address: Mapped[str] = mapped_column(String(200))
    max_room: Mapped[int] = mapped_column(Integer)
    image: Mapped[Optional[str]] = mapped_column(String(256))

    rooms: Mapped[List['Room']] = relationship(back_populates="motel",
                                               cascade="all, delete-orphan")
    user_id: Mapped[str] = mapped_column(ForeignKey(User.id))
    user: Mapped['User'] = relationship(back_populates="motels")

    def __repr__(self):
        return f'<Motel {self.address}>'


# Room model
class Room(db.Model):
    __tablename__ = "rooms"

    id: Mapped[str] = mapped_column(String(36), primary_key=True,
                                    default=uuid4())
    room_name: Mapped[str] = mapped_column(String(100))
    base_price: Mapped[float] = mapped_column(Float)
    description: Mapped[Optional[str]] = mapped_column(Text)
    water_price: Mapped[float] = mapped_column(Float)
    electric_price: Mapped[float] = mapped_column(Float)
    picture: Mapped[Optional[str]] = mapped_column(String(256))

    motel_id: Mapped[str] = mapped_column(ForeignKey(Motel.id))
    motel: Mapped['Motel'] = relationship(back_populates="rooms")

    posts: Mapped[List['Post']] = relationship(back_populates="room",
                                               cascade="all, delete-orphan")
    bookings: Mapped[List['Booking']] = relationship(back_populates="room")
    reviews: Mapped[List['Review']] = relationship(back_populates="room")

    def __repr__(self):
        return f'<Room {self.room_name}>'


# Post model
class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True,
                                    default=str(uuid4()))
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(
        index=True,
        default=lambda: datetime.now(tz=ZoneInfo("Asia/Ho_Chi_Minh"))
    )


    user_id: Mapped[str] = mapped_column(ForeignKey(User.id))
    room_id: Mapped[str] = mapped_column(ForeignKey(Room.id))

    author: Mapped['User'] = relationship(back_populates='posts')
    room: Mapped['Room'] = relationship(back_populates='posts')

    post_images: Mapped[List['PostImage']] = relationship(
        back_populates='post', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Post {self.title}>'


# Booking model
class Booking(db.Model):
    __tablename__ = 'bookings'

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4())
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="Pending")
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    room_id: Mapped[str] = mapped_column(ForeignKey('rooms.id'))

    user: Mapped['User'] = relationship('User', back_populates='bookings')
    room: Mapped['Room'] = relationship('Room', back_populates='bookings')

    def __repr__(self):
        return f'<Booking {self.id}>'




# Review model
class Review(db.Model):
    __tablename__ = "reviews"

    id: Mapped[str] = mapped_column(String(36),
                                    primary_key=True, default=uuid4())
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[Optional[str]] = mapped_column(Text)

    user_id: Mapped[str] = mapped_column(ForeignKey(User.id))
    room_id: Mapped[str] = mapped_column(ForeignKey(Room.id))

    user: Mapped['User'] = relationship(back_populates="reviews")
    room: Mapped['Room'] = relationship(back_populates="reviews")

    def __repr__(self):
        return f'<Review {self.rating}>'


class PostImage(db.Model):
    __tablename__ = "post_images"
    id: Mapped[str] = mapped_column(String(36),
                                    primary_key=True, default=str(uuid4()))
    image_path: Mapped[str] = mapped_column(String(256))

    post_id: Mapped[str] = mapped_column(ForeignKey(Post.id))

    post: Mapped['Post'] = relationship(back_populates="post_images")


class PostImage(db.Model):
    __tablename__ = "post_images"
    id: Mapped[str] = mapped_column(String(36),
                                    primary_key=True, default=str(uuid4()))
    image_path: Mapped[str] = mapped_column(String(256))

    post_id: Mapped[str] = mapped_column(ForeignKey(Post.id))

    post: Mapped['Post'] = relationship(back_populates="post_images")


# Payment model
# Payment model
# class Payment(db.Model):
#     __tablename__ = "payments"
# 
#     id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4())
#     amount: Mapped[float] = mapped_column(Float)
#     status: Mapped[str] = mapped_column(String(20), default='Pending')
# 
#     booking_id: Mapped[str] = mapped_column(ForeignKey(Booking.id))
#     booking: Mapped['Booking'] = relationship()
# 
#     def __repr__(self):
#         return f'<Payment {self.id}>'


# Message model
class Message(db.Model):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4())
    content: Mapped[str] = mapped_column(Text)

    sender_id: Mapped[str] = mapped_column(ForeignKey(User.id))
    receiver_id: Mapped[str] = mapped_column(ForeignKey(User.id))

    sender: Mapped['User'] = relationship('User', foreign_keys=[sender_id], back_populates="messages_sent")
    receiver: Mapped['User'] = relationship('User', foreign_keys=[receiver_id], back_populates="messages_received")

    def __repr__(self):
        return f'<Message {self.id}>'


