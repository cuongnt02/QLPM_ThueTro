from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import TextAreaField, FileField, RadioField, DecimalField
from wtforms import SelectField, MultipleFileField, DateTimeField
from wtforms import DecimalRangeField
from wtforms.validators import DataRequired, Email, Optional, Length
from wtforms.validators import EqualTo, ValidationError, NumberRange
from app.models import User
from app import db
from app import app
from sqlalchemy import select
from enum import Enum

icon_map = {
        'username': 'fas fa-user',
        'password': 'fas fa-key',
        'full_name': 'fas fa-user',
        'repeat_password': 'fas fa-key',
        'avatar': 'fas fa-image',
        'email': 'fas fa-envelope',
        'address': 'fas fa-home'
}


@app.template_filter('icon')
def icon_filter(field_name):
    icon_class = icon_map.get(field_name, '')
    return icon_class


@app.template_filter()
def to_string(obj):
    if isinstance(obj, Enum):
        return obj.value
    return obj



class LoginForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    role = RadioField(choices=['Khách hàng', 'ADMIN'])
    remember_me = BooleanField('Ghi nhớ đăng nhập')
    submit = SubmitField('Đăng nhập')


class RegisterForm(FlaskForm):
    username = StringField('Tên tài khoản', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Họ và tên', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    repeat_password = PasswordField(
            'Xác nhận mật khẩu',
            validators=[DataRequired(), EqualTo('password')])
    avatar = FileField('Avatar', validators=[DataRequired()])
    submit = SubmitField('Đăng ký')

    def validate_username(self, username):
        user = db.session.scalar(select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Tên tài khoản đã tồn tại')

    def validate_email(self, email):
        email = db.session.scalar(select(User).where(
            User.email == email.data))
        if email is not None:
            raise ValidationError('Email đã tồn tại')


class UserEditForm(FlaskForm):
    username = StringField('Tên tài khoản', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    full_name = StringField('Họ Tên', validators=[DataRequired()])
    phone_number = StringField('SDT', validators=[Optional(), Length(10, 11)])
    address = StringField('Địa chỉ', validators=[Optional()])
    avatar = FileField('Avatar')
    submit = SubmitField('Lưu thông tin')


class CommentForm(FlaskForm):
    content = TextAreaField('Điền bình luận', validators=[DataRequired()])
    rating = DecimalRangeField('Đánh giá', validators=[NumberRange(min=0.0, max=5.0)])
    submit = SubmitField('Lưu')


class MotelEditForm(FlaskForm):
    address = StringField('Địa chỉ', validators=[DataRequired()])
    motel_image = FileField('Hình ảnh', validators=[Optional()])
    submit = SubmitField('Lưu thông tin')


class MotelCreateForm(FlaskForm):
    address = StringField('Địa chỉ', validators=[DataRequired()])
    motel_image = FileField('Hình ảnh', validators=[DataRequired()])
    submit = SubmitField('Tạo nhà trọ')


class RoomCreateForm(FlaskForm):
    room_name = StringField('Tên phòng', validators=[DataRequired()])
    base_price = DecimalField('Giá cơ bản', validators=[DataRequired()])
    description = StringField('Mô tả', validators=[DataRequired()])
    water_price = DecimalField('Giá nước', validators=[DataRequired()])
    electric_price = DecimalField('Giá điện', validators=[DataRequired()])
    picture = FileField('Hình ảnh mô tả', validators=[DataRequired()])
    submit = SubmitField('Tạo phòng')


class RoomEditForm(FlaskForm):
    room_name = StringField('Tên phòng', validators=[DataRequired()])
    base_price = DecimalField('Giá cơ bản', validators=[DataRequired()])
    description = StringField('Mô tả', validators=[DataRequired()])
    water_price = DecimalField('Giá nước', validators=[DataRequired()])
    electric_price = DecimalField('Giá điện', validators=[DataRequired()])
    picture = FileField('Hình ảnh mô tả', validators=[Optional()])
    submit = SubmitField('Chỉnh sửa phòng')


class PostCreateForm(FlaskForm):
    post_title = StringField('Tiêu đề', validators=[DataRequired()])
    content = TextAreaField('Nội dung', validators=[DataRequired()])
    room = SelectField('Room', validators=[DataRequired()])
    gallery = MultipleFileField('Hình ảnh', validators=[Optional()])
    submit = SubmitField('Tạo bài đăng')


class PostEditForm(FlaskForm):
    post_title = StringField('Tiêu đề', validators=[DataRequired()])
    content = TextAreaField('Nội dung', validators=[DataRequired()])
    room = SelectField('Room', validators=[DataRequired()])
    gallery = MultipleFileField('Hình ảnh', validators=[Optional()])
    submit = SubmitField('Tạo bài đăng')


class BookingForm(FlaskForm):
    start_date = DateTimeField('Ngày đặt')
    end_date = DateTimeField('Ngày hẹn trả')
    total_price = DecimalField('Giá cọc')
    submit = SubmitField('Đặt cọc')
