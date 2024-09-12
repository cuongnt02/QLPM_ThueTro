from urllib.parse import urlsplit
from uuid import uuid4

import paypalrestsdk
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import select
from cloudinary import uploader

from app import app, db
from app.models import User, Post, Motel, Room, UserRole, Booking, Payment
from app.forms import LoginForm, RegisterForm, UserEditForm, CommentForm
from app.forms import MotelEditForm, MotelCreateForm, RoomCreateForm
from app.forms import PostCreateForm, BookingForm
from app.forms import RoomEditForm
from app.utils import require_roles

paypalrestsdk.configure({
    "mode": "sandbox",  # hoặc "live" để dùng trên môi trường sản xuất
    "client_id": "ARjB0Vl_utFQqmJzoM7ABib94XnH8q63urVLtrlvEgQkT_c_cZtYwHhSh7dvaQflMQ0NgeyzTqixSMDx",
    "client_secret": "ENNui3hmj9i59mHjp-VHr-Rm8PuWxVIlm6Ukb9deeiOnvnrQ3YK--0XBhVF_a_54DTmfab4pFEXBDlQZ"
})


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
        if form.role.data == 'ADMIN':
            if user.user_role == UserRole.ADMIN:
                return redirect(url_for('admin'))
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
        avatar_path = None
        if form.avatar.data:
            image = request.files[form.avatar.name]
            if image:
                response = uploader.upload(image)
                avatar_path = response['secure_url']
                user.avatar = avatar_path
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
    form = BookingForm()  # Thêm dòng này để khởi tạo form
    return render_template("room_detail.html",
                           title="Chi tiết phòng", room=room, form=form)

@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html")



@app.route("/room/<room_id>/edit", methods=['GET', 'POST'])
def edit_room(room_id):
    form = RoomEditForm()
    room = db.session.scalar(select(Room).where(Room.id == room_id))
    if form.validate_on_submit():
        room.room_name = form.room_name.data
        room.base_price = form.base_price.data
        room.description = form.description.data
        room.water_price = form.water_price.data
        room.electric_price = form.electric_price.data
        image_path = None
        if form.picture.data:
            picture = request.files[form.picture.name]
            if picture:
                response = uploader.upload(picture)
                image_path = response['secure_url']
                room.picture = image_path
        db.session.add(room)
        db.session.commit()
        flash('Chỉnh sửa phòng thành công')
        return redirect(url_for('edit_motel', motel_id=room.motel.id))

    elif request.method == 'GET':
        form.room_name.data = room.room_name
        form.base_price.data = room.base_price
        form.description.data = room.description
        form.water_price.data = room.water_price
        form.electric_price.data = room.electric_price

    return render_template("room_edit.html", form=form,
                           title="Chỉnh sửa phòng", room=room)


@app.route("/motel/<motel_id>/create", methods=['GET', 'POST'])
def create_room(motel_id):
    form = RoomCreateForm()
    motel = db.session.scalar(select(Motel).where(Motel.id == motel_id))
    if form.validate_on_submit():
        room = Room(id=str(uuid4()),
                    room_name=form.room_name.data,
                    base_price=form.base_price.data,
                    description=form.description.data,
                    water_price=form.water_price.data,
                    electric_price=form.electric_price.data,
                    motel_id=motel.id)
        picture_path = None
        if form.picture.data:
            picture = request.files[form.picture.name]
            if picture:
                response = uploader.upload(picture)
                picture_path = response['secure_url']
                room.picture = picture_path
        db.session.add(room)
        db.session.commit()
        flash("Tạo phòng thành công")
    return render_template("room_create.html", form=form,
                           title="Tạo phòng", motel=motel)


@app.route("/motel/delete/<motel_id>", methods=['DELETE'])
def delete_motel(motel_id):
    motel = db.session.scalar(select(Motel).where(Motel.id == motel_id))
    if motel:
        db.session.delete(motel)
        db.session.commit()
        return jsonify({'message': 'Motel deleted successfully'}), 200
    else:
        return jsonify({'error': 'Motel not exist'}), 404


@app.route("/room/delete/<room_id>", methods=['DELETE'])
def delete_room(room_id):
    room = db.session.scalar(select(Room).where(Room.id == room_id))
    if room:
        db.session.delete(room)
        db.session.commit()
        return jsonify({'message': 'Room deleted successfully'}), 200
    else:
        return jsonify({'error': 'Room not exist'}), 404


@app.route("/post/<post_id>/comment", methods=['GET', 'POST'])
@login_required
def comment(post_id):
    form = CommentForm()
    post = db.session.scalar(select(Post).where(Post.id == post_id))
    return render_template("comment.html", title="Bình luận", form=form,
                           post=post)


@app.route("/motel/manage", methods=['GET'])
@login_required
@require_roles(UserRole.LANDLORD)
def manage_motel():
    motels = db.session.scalars(select(Motel))
    return render_template("motels.html", title="Quản lý phòng trọ",
                           motels=motels)


@app.route("/motel/<motel_id>/edit", methods=['GET', 'POST'])
@login_required
@require_roles(UserRole.LANDLORD)
def edit_motel(motel_id):
    form = MotelEditForm()
    motel = db.session.scalar(select(Motel).where(Motel.id == motel_id))
    if form.validate_on_submit():
        motel.address = form.address.data
        image_path = None
        if form.motel_image.data:
            image = request.files[form.motel_image.name]
            if image:
                response = uploader.upload(image)
                image_path = response['secure_url']
                motel.image = image_path
        db.session.add(motel)
        db.session.commit()
        flash("Chỉnh sửa nhà trọ thành công")
        return redirect(url_for('manage_motel'))
    elif request.method == 'GET':
        form.address.data = motel.address
    return render_template("motel_edit.html", title="Chỉnh sửa nhà trọ",
                           motel=motel, form=form)


@app.route("/motel/create", methods=['GET', 'POST'])
@login_required
@require_roles(UserRole.LANDLORD)
def create_motel():
    form = MotelCreateForm()
    if form.validate_on_submit():
        motel = Motel(id=str(uuid4()),
                      address=form.address.data,
                      max_room=0,
                      user_id=current_user.id)
        image_path = None
        if form.motel_image.data:
            image = request.files[form.motel_image.name]
            if image:
                response = uploader.upload(image)
                image_path = response['secure_url']
                motel.image = image_path
        db.session.add(motel)
        db.session.commit()
        flash("Tạo nhà trọ thành công")
        return redirect(url_for('manage_motel'))
    return render_template("motel_create.html", form=form, title="Tạo nhà trọ")


@app.route("/motel/<motel_id>", methods=['GET'])
def motel(motel_id):
    motel = db.session.scalar(select(Motel).where(Motel.id == motel_id))
    return render_template("motel_info.html",
                           title="Thông tin nhà trọ", motel=motel)


@app.route("/user/<username>/create", methods=['GET', 'POST'])
@login_required
@require_roles(UserRole.LANDLORD)
def create_post(username):
    form = PostCreateForm()
    user = db.first_or_404(select(User).where(User.username == username))
    motels = db.session.scalars(select(Motel).where(Motel.user_id == user.id))
    rooms = []
    for motel in motels:
        for room in motel.rooms:
            rooms.append(room)
    room_list = [(room.id, room.room_name) for room in rooms]
    form.room.choices = room_list
    if form.validate_on_submit():
        post = Post(id=str(uuid4()),
                    title=form.post_title.data,
                    content=form.content.data,
                    user_id=user.id,
                    room_id=form.room.data)
        db.session.add(post)
        db.session.commit()
        gallery = request.files.getlist(form.gallery.name)
        if gallery:
            for image in gallery:
                postimage = PostImage(id=str(uuid4()))
                if image:
                    response = uploader.upload(image)
                    postimage.image_path = response['secure_url']
                postimage.post_id = post.id
                db.session.add(postimage)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template("post_create.html", user=user, form=form)


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




@app.route("/contracts", methods=['GET'])
def contract():
    return render_template("contracts.html")


@app.route("/room/<room_id>/booking", methods=['POST'])
def booking(room_id):
    room = db.session.scalar(select(Room).where(Room.id == room_id))

    if not room:
        flash('Phòng không tồn tại')
        return redirect(url_for('home'))

    # Tạo yêu cầu thanh toán với PayPal
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": url_for('payment_execute', room_id=room.id, _external=True),
            "cancel_url": url_for('payment_cancel', room_id=room.id, _external=True)},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": room.room_name,
                    "sku": str(room.id),
                    "price": f'{room.base_price:.2f}',
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": f'{room.base_price:.2f}',
                "currency": "USD"},
            "description": f"Đặt phòng: {room.room_name}"}]})

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        flash(f"Đã xảy ra lỗi: {payment.error}")
        return redirect(url_for('room', room_id=room_id))


@app.route('/payment/execute', methods=['GET'])
@app.route('/payment/execute/<room_id>', methods=['GET'])
def payment_execute(room_id):
    payment_id = request.args.get('orderID')
    payer_id = request.args.get('payerID')

    try:
        # Tìm đơn đặt phòng
        booking = Booking.query.filter_by(room_id=room_id, status="Pending").first()
        if not booking:
            flash('Không tìm thấy đơn đặt phòng.', 'danger')
            return redirect(url_for('home', room_id=room_id))

        # Cập nhật trạng thái thanh toán và lưu thông tin từ PayPal
        payment = Payment.query.filter_by(booking_id=booking.id).first()
        if payment:
            payment.payment_id = payment_id
            payment.payer_id = payer_id
            payment.status = 'Completed'
            db.session.commit()  # Lưu thay đổi vào cơ sở dữ liệu
            flash('Thanh toán thành công!', 'success')
        else:
            flash('Không tìm thấy giao dịch thanh toán.', 'danger')

    except Exception as e:
        db.session.rollback()  # Rollback nếu có lỗi
        flash(f"Đã xảy ra lỗi: {e}", 'danger')

    return redirect(url_for('home', room_id=room_id))


@app.route('/payment/cancel', methods=['GET'])
def payment_cancel():
    # Xử lý khi thanh toán bị hủy
    return "Thanh toán bị hủy"


@app.route("/receipt/<room_id>", methods=['GET'])
def receipt(room_id):
    room = db.session.scalar(select(Room).where(Room.id == room_id))
    if room:
        return render_template("receipt.html", room=room, title="Hóa đơn")
    else:
        flash('Phòng không tồn tại')
        return redirect(url_for('home'))


@app.route("/booking", methods=['GET'])
def booking_page():
    return render_template("booking.html", title="Đặt phòng")




