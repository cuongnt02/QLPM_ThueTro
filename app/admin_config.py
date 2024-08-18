from app import app, db, admin
from app.models import User, Post, Motel, Room
from flask_admin.contrib.sqla import ModelView


admin.add_view(ModelView(User, db.session, endpoint='user'))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Motel, db.session))
admin.add_view(ModelView(Room, db.session))
