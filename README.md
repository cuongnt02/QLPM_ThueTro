# QLPM_ThueTro

## Sử dụng

### Tạo môi trường ảo

``` bash
python -m virtualenv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Tích hợp database
1. Tạo một database trong mysql (tên mặc định là thuetro)
2. Thay đổi giá trị mật khẩu mysql khớp với tài khoản trên máy tính
3. chạy các lệnh
``` bash
flask db upgrade
```
4. Mỗi khi pull về chạy lệnh
``` bash
flask db downgrade base
flask db upgrade
```
5. Tạo data giả trên database
``` bash
python data.py
```
Lưu ý là database phải tạo xong mới thêm data được
6. Thay đổi biến môi trường
- Mở file .flaskenv
- Thay đổi biến DATABASE_URI
DATABASE_URI=mysql+pymysql://root:**matkhau**@localhost/thuetro?charset=utf8mb4
Đổi **matkhau** thành mật khẩu mysql server đã cài đặt

### Chạy app
``` bash
flask run
```
