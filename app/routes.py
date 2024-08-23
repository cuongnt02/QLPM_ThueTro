from urllib.parse import urlsplit
from uuid import uuid4
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import select
from cloudinary import uploader

from app import app, db
from app.models import User, Post, Motel, Room, UserRole
from app.forms import LoginForm, RegisterForm, UserEditForm, CommentForm
from app.utils import require_roles


@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    posts = db.session.scalars(select(Post)).all()
    keyword = request.args.get('title')
    if keyword is not None and keyword != '':
        posts = db.session.scalars(select(Post).where(
                Post.title.like('%{}%'.format(keyword)))).all()
    return render_template('home.html', title="Trang chủ", posts=posts)


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


@app.route("/post/<post_id>", methods=['GET'])
def post(post_id):
    post = db.session.scalar(select(Post).where(Post.id == post_id))
    return render_template("post_info.html",
                           title="Bài viết", post=post)


@app.route("/room/<room_id>", methods=['GET'])
def room(room_id):
    room = db.session.scalar(select(Room).where(Room.id == room_id))
    return render_template("room_detail.html",
                           title="Chi tiết phòng", room=room)


@app.route("/post/<post_id>/comment", methods=['GET', 'POST'])
@login_required
def comment(post_id):
    form = CommentForm()
    post = db.session.scalar(select(Post).where(Post.id == post_id))
    return render_template("comment.html", title="Bình luận", form=form,
                           post=post)


@app.route("/motel/manage", methods=['GET'])
@login_required
@require_roles(UserRole.OWNER)
def manage_motel():
    return "manage motel"


@app.route("/motel/<motel_id>", methods=['GET'])
def motel(motel_id):
    motel = db.session.scalar(select(Motel).where(Motel.id == motel_id))
    return render_template("motel_info.html",
                           title="Thông tin nhà trọ", motel=motel)


@app.route("/user/<username>")
@login_required
def user(username):
    user = db.first_or_404(select(User).where(User.username == username))
    return render_template("user.html", user=user)


@app.route("/user/<username>/edit", methods=['GET', 'POST'])
@login_required
def user_edit(username):
    user = db.first_or_404(select(User).where(User.username == username))
    form = UserEditForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.full_name = form.full_name.data
        current_user.phone_number = form.phone_number.data
        current_user.address = form.address.data
        avatar_path = None

        if form.avatar.data:
            image = request.files[form.avatar.name]
            if image:
                response = uploader.upload(image)
                avatar_path = response['secure_url']
                current_user.avatar = avatar_path
        db.session.commit()
        flash('Thông tin đã được lưu')
        return redirect(url_for('user', username=username))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.full_name.data = user.full_name
        form.phone_number.data = user.phone_number
        form.address.data = user.address
    return render_template("user_edit.html", user=user, form=form)


@app.route("/about", methods=['GET'])
def about():
    return "about_page"


@app.route("/contracts", methods=['GET'])
def contract():
    return render_template("contracts.html")


@app.route("/booking", methods=['GET'])
def booking():
    return render_template("booking.html")


@app.route("/receipt", methods=['GET'])
def receipt():
    return render_template("receipt.html")
