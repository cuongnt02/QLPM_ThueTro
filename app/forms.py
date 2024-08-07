from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User
from app import db
from sqlalchemy import select


class LoginForm(FlaskForm):
    username = StringField('Tên tài khoản', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
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
