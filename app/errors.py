from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(401)
def unauthorize_error(error):
    return render_template('401.html'), 401


@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403
