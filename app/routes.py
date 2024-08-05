from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm


@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    title = "Trang chủ"
    return render_template('home.html', title=title)


@app.route("/login", methods=['GET', 'POST'])
def login():
    title = "Đăng nhập"
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login Requested for user {}".format(form.username.data))
        return redirect('/home')
    return render_template('login.html', title=title, form=form)
