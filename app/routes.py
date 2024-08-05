from app import app
from flask import render_template


@app.route('/')
@app.route('/home')
def home():
    title = "Trang chủ"
    return render_template('home.html', title=title)
