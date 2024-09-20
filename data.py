from uuid import uuid4
from datetime import datetime, timedelta
import pytz
from app import app, db
from app.models import User, Motel, Room, Post, Review, Payment, Message, Booking
from sqlalchemy.exc import IntegrityError

def create_user(username, email, full_name, password, role):
    user = User(
        id=uuid4(),
        username=username,
        email=email,
        full_name=full_name,
        user_role=role
    )
    user.set_password(password)
    return user

def create_motel(address, max_room, user_id):
    return Motel(
        id=uuid4(),
        address=address,
        max_room=max_room,
        user_id=user_id,
    )

def create_room(room_name, base_price, description, water_price,
                electric_price, motel_id, picture=""):
    return Room(
        id=uuid4(),
        room_name=room_name,
        base_price=base_price,
        description=description,
        water_price=water_price,
        electric_price=electric_price,
        picture=picture,
        motel_id=motel_id
    )

def create_post(title, content, user_id, room_id, timezone):
    current_time = datetime.now(timezone)
    return Post(
        id=uuid4(),
        title=title,
        content=content,
        timestamp=current_time,
        user_id=user_id,
        room_id=room_id
    )

def create_booking(user_id, room_id, start_date, end_date, total_price):
    return Booking(
        id=uuid4(),
        start_date=start_date,
        end_date=end_date,
        total_price=total_price,
        user_id=user_id,
        room_id=room_id
    )

def create_review(user_id, room_id, rating, comment):
    return Review(
        id=uuid4(),
        rating=rating,
        comment=comment,
        user_id=user_id,
        room_id=room_id
    )

def create_message(sender_id, receiver_id, content):
    return Message(
        id=uuid4(),
        content=content,
        sender_id=sender_id,
        receiver_id=receiver_id
    )

if __name__ == "__main__":

    with app.app_context():

        # Tạo users
        u1 = create_user("cuong", "cuong@gmail.com", "NTC", "123456", "USER")
        u2 = create_user("an", "an@gmail.com", "NCPA", "123456", "USER")
        u3 = create_user("admin", "admin@gmail.com", "Admin", "admin123", "ADMIN")

        db.session.add_all([u1, u2, u3])

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print("Lỗi: Không thể thêm người dùng do trùng lặp email.")

        # Tạo motels
        # m1 = create_motel(address="Go Vap, Ho Chi Minh", max_room=3, user_id=u2.id)
        # m2 = create_motel(address="Phu Nhuan, Ho Chi Minh", max_room=4, user_id=u2.id)
        # db.session.add_all([m1, m2])
        # db.session.commit()

        # Tạo rooms
        # r1 = create_room("Phòng 101", 2000000, "Phòng trọ thoáng mát, gần siêu thị, sân bay.", 100000, 100000, m1.id, picture="https://res.cloudinary.com/driiz3taz/image/upload/v1724417992/Working/tro1_uqndaa.jpg")
        # r2 = create_room("Phòng 102", 2500000, "Phòng trọ thoáng mát, gần siêu thị, sân bay.", 150000, 150000, m1.id, picture="https://res.cloudinary.com/driiz3taz/image/upload/v1724417990/Working/tro2_imkkzq.jpg")
        # r3 = create_room("Phòng 201", 3000000, "Phòng rộng, tiện nghi.", 120000, 120000, m2.id, picture="https://res.cloudinary.com/driiz3taz/image/upload/v1724417989/Working/tro3_fnnjli.jpg")
        # db.session.add_all([r1, r2, r3])
        # db.session.commit()

        # Sử dụng múi giờ 'Asia/Ho_Chi_Minh'
        # timezone = pytz.timezone('Asia/Ho_Chi_Minh')

        # Tạo posts
        # p1 = create_post("Phòng trọ tại Gò Vấp", r1.description, u1.id, r1.id, timezone)
        # p2 = create_post("Phòng trọ tại Phú Nhuận", r2.description, u1.id, r2.id, timezone)
        # p3 = create_post("Phòng trọ rộng tại Phú Nhuận", r3.description, u2.id, r3.id, timezone)
        # db.session.add_all([p1, p2, p3])
        # db.session.commit()

        # Tạo bookings
        # b1 = create_booking(u1.id, r1.id, datetime.now(), datetime.now() + timedelta(days=30), 6000000)
        # b2 = create_booking(u2.id, r2.id, datetime.now(), datetime.now() + timedelta(days=15), 3750000)
        # db.session.add_all([b1, b2])
        # db.session.commit()

        # Tạo reviews
        # rev1 = create_review(u1.id, r1.id, 4, "Phòng tốt nhưng hơi ồn.")
        # rev2 = create_review(u2.id, r2.id, 5, "Phòng rất tốt, sạch sẽ.")
        # db.session.add_all([rev1, rev2])
        # db.session.commit()

        # Tạo payments

        # Tạo messages
        # msg1 = create_message(u1.id, u2.id, "Xin chào, phòng còn trống không?")
        # msg2 = create_message(u2.id, u1.id, "Xin chào, phòng còn trống. Bạn muốn thuê khi nào?")
        # db.session.add_all([msg1, msg2])
        # db.session.commit()

        print("Dữ liệu đã được thêm thành công!")
