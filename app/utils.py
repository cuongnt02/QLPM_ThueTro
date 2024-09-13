from functools import wraps
from flask_login import current_user
from werkzeug.exceptions import Unauthorized, Forbidden


def require_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def authorize(*args, **kwargs):
            if not current_user.is_authenticated:
                raise Unauthorized()
            if current_user.user_role not in roles:
                raise Forbidden()

            return f(*args, **kwargs)
        return authorize
    return wrapper
