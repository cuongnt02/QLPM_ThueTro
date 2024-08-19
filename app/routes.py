from urllib.parse import urlsplit
from uuid import uuid4
from werkzeug.datastructures import MultiDict
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import select

from app import app, db
from app.models import User, Post, Motel, Room, UserRole
from app.forms import LoginForm, RegisterForm, UserEditForm


@app.route('/', methods=['GET', 'POST'])
def home():
    posts = db.session.scalars(select(Post)).all()
    keyword = request.args.get('title')
    if keyword:
        posts = db.session.scalars(select(Post).where(
            Post.title.like(f'%{keyword}%'))).all()
    return render_template('home.html', title="Trang chủ", posts=posts)

@app.route('/about', methods=['GET', 'POST'])
def about():
   return "ahha"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user=user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title="Đăng nhập", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            id=str(uuid4()),
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Đăng ký thành công')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title="Đăng kí")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/room/<room_id>')
def room_detail(room_id):
    room = Room.query.get_or_404(room_id)
    return render_template('room_detail.html', room=room)


@app.route("/motel/<motel_id>")
def motel(motel_id):
    motel = db.session.scalar(select(Motel).where(Motel.id == motel_id))
    return render_template("motel_info.html", title="Thông tin nhà trọ", motel=motel)


@app.route("/user/<username>")
@login_required
def user(username):
    user = db.session.scalar(select(User).where(User.username == username))
    return render_template("user.html", user=user)


@app.route("/user/<username>/edit", methods=['GET', 'POST'])
@login_required
def user_edit(username):
    user = db.session.scalar(select(User).where(User.username == username))
    if user != current_user and current_user.user_role != UserRole.ADMIN:
        flash('Bạn không có quyền chỉnh sửa thông tin của người dùng khác.')
        return redirect(url_for('user', username=username))

    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.full_name = form.full_name.data
        user.phone_number = form.phone_number.data
        user.address = form.address.data
        db.session.commit()
        flash('Thông tin của bạn đã được cập nhật.')
        return redirect(url_for('user', username=user.username))

    return render_template("user_edit.html", user=user, form=form)
