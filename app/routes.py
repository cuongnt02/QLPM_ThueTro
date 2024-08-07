from urllib.parse import urlsplit
from uuid import uuid4

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import select

from app import app, db
from app.models import User
from app.forms import LoginForm, RegisterForm


@app.route('/')
@app.route('/home')
@app.route('/index')
@login_required
def home():
    title = "Trang chủ"
    return render_template('home.html', title=title)


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
