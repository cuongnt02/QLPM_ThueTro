from uuid import uuid4

from app import app, db
from app.models import Room, Motel, User, Post


if __name__ == "__main__":

    app_context = app.app_context()
    app_context.push()

    db.create_all()

    # User data
    u1 = User(id=uuid4(), username="cuong", email="cuong@gmail.com",
              full_name="NTC")
    u1.set_password("123456")
    u2 = User(id=uuid4(), username="an", email="an@gmail.com",
              full_name="NCPA")
    u2.set_password("123456")

    db.session.add_all([u1, u2])
    db.session.commit()

    # Motel data
    m1 = Motel(id=uuid4(), address="Go Vap, Ho Chi Minh", max_room=3)
    m2 = Motel(id=uuid4(), address="Phu Nhuan, Ho Chi Minh", max_room=4)
    db.session.add_all([m1, m2])
    db.session.commit()

    # Room data
    r1 = Room(id=uuid4(), room_name="Phòng 101", base_price=2000000,
              description="Phòng trọ thoáng mát, gần siêu thị, sân bay.",
              water_price=100000, electric_price=100000, picture="",
              motel_id=m1.id)
    r2 = Room(id=uuid4(), room_name="Phòng 102", base_price=2500000,
              description="Phòng trọ thoáng mát, gần siêu thị, sân bay.",
              water_price=150000, electric_price=150000, picture="",
              motel_id=m1.id)
    r3 = Room(id=uuid4(), room_name="Phòng 103", base_price=2200000,
              description="Phòng trọ thoáng mát, gần siêu thị, sân bay.",
              water_price=120000, electric_price=120000, picture="",
              motel_id=m1.id)
    db.session.add_all([r1, r2, r3])
    db.session.commit()

    # Post data
    p1 = Post(id=uuid4(), title="Phòng trọ tại Gò Vấp, Hồ Chí Minh",
              content=r1.description, user_id=u1.id, room_id=r1.id)
    p2 = Post(id=uuid4(), title="Phòng trọ tại Phú Nhuận, Hồ Chí Minh",
              content=r2.description, user_id=u1.id, room_id=r2.id)
    p3 = Post(id=uuid4(), title="Phòng trọ tại Tân Bình, Hồ Chí Minh",
              content=r3.description, user_id=u2.id, room_id=r3.id)
    db.session.add_all([p1, p2, p3])
    db.session.commit()

    db.session.remove()
    app_context.pop()
