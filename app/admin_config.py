from app import db, app
from app.models import User, Post, Motel, Room, UserRole, Booking, Review
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from flask_admin.base import AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, abort
from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme
from flask_admin.base import expose
from app.utils import require_roles


class AdminIndex(AdminIndexView):

    @require_roles(UserRole.ADMIN)
    @expose('/')
    def index(self):
        return super(AdminIndex, self).index()


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


class CustomReviewReport(BaseView):
    @expose('/', methods=['GET'])
    def reviews_by_user(self):
        results = db.session.query(
            User.full_name.label('user_name'),
            db.func.count(Review.id).label('total_reviews')
        ).outerjoin(Review, User.id == Review.user_id) \
         .group_by(User.id) \
         .all()

        # Chuẩn bị dữ liệu JSON để gửi đến template
        labels = [user_name for user_name, _ in results]
        values = [total_reviews for _, total_reviews in results]

        # Return JSON data to template
        return self.render('admin/stats.html',
                           output={'labels': labels, 'values': values})


class BookingReport(BaseView):
    @expose('/', methods=['GET'])
    def total_bookings_by_day(self):
        results = db.session.query(
            db.func.date(Booking.start_date).label('date'),
            db.func.count(Booking.id).label('total_bookings')
        ).group_by(db.func.date(Booking.start_date)) \
         .all()
        labels = [date.strftime('%Y-%m-%d') for date, _ in results]
        values = [count for _, count in results]

        # Return JSON data to template
        return self.render('admin/stats.html',
                           output={'labels': labels, 'values': values})


class MotelReport(BaseView):
    @expose('/', methods=['GET'])
    def rooms_by_motel(self):
        results = db.session.query(
            Motel.address.label('motel_address'),
            db.func.count(Room.id).label('total_rooms')
        ).outerjoin(Room, Motel.id == Room.motel_id) \
         .group_by(Motel.id) \
         .all()

        labels = [motel_address for motel_address, _ in results]
        values = [total_rooms for _, total_rooms in results]

        # Return JSON data to template
        return self.render('admin/stats.html',
                           output={'labels': labels, 'values': values})

class PostReport(BaseView):
    @expose('/', methods=['GET'])
    def posts_by_room(self):
        results = db.session.query(
            Room.room_name.label('room_name'),
            db.func.count(Post.id).label('total_posts')
        ).outerjoin(Post, Room.id == Post.room_id) \
         .group_by(Room.id) \
         .all()

        # Chuẩn bị dữ liệu để trả về JSON
        labels = [room_name for room_name, _ in results]
        values = [total_posts for _, total_posts in results]

        # Return JSON data to template
        return self.render('admin/stats.html', output={'labels': labels, 'values': values})


class ReviewReport(BaseView):
    @expose('/', methods=['GET'])
    def average_rating_by_room(self):
        results = db.session.query(
            Room.room_name.label('room_name'),
            db.func.avg(Review.rating).label('average_rating')
        ).outerjoin(Review, Room.id == Review.room_id) \
         .group_by(Room.id) \
         .all()

        # Chuẩn bị dữ liệu JSON để gửi đến template
        labels = [room_name for room_name, _ in results]
        values = [average_rating for _, average_rating in results]

        # Return JSON data to template
        return self.render('admin/stats.html',
                           output={'labels': labels, 'values': values})


class RevenueReport(BaseView):
    @expose('/', methods=['GET'])
    def total_revenue_by_day(self):
        results = db.session.query(
            db.func.date(Booking.start_date).label('day'),
            db.func.sum(Booking.total_price).label('total_revenue')
        ).group_by(db.func.date(Booking.start_date)).all()

        # Chuẩn bị dữ liệu JSON để gửi đến template
        labels = [str(day) for day, _ in results]
        values = [total_revenue for _, total_revenue in results]

        # Return JSON data to template
        return self.render('admin/stats.html', output={'labels': labels, 'values': values})


admin = Admin(app, name='THUETRO ADMIN', index_view=AdminIndex(),
              theme=Bootstrap4Theme(swatch='cyborg'))

# Add CustomModelView to the admin interface
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Booking, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Motel, db.session))
admin.add_view(ModelView(Room, db.session))
admin.add_view(CustomReviewReport(name='Thông kê đánh giá của người dùng'))
admin.add_view(BookingReport(name='Thong ke dat phong '))
admin.add_view(MotelReport(name='Thong ke nha tro'))
admin.add_view(PostReport(name='Thong ke bai dang'))
admin.add_view(ReviewReport(name='Thong ke danh gia'))
admin.add_view(RevenueReport(name='thong ke doanh thu'))
admin.add_view(LogoutView(name='Đăng xuất'))
