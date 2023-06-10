from functools import wraps
from flask import  app,session, redirect, url_for,render_template,current_app
from flask_pymongo import PyMongo

mongo = PyMongo(app)

def email_session_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('ret_login'))
        return route_function(*args, **kwargs)
    return wrapper

def email_session_found(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if 'email' in session:
            db = mongo.db
            user = db.admins.find_one({"email":session['email']})
            return route_function(*args, **kwargs)
        else:
            return render_template('login_page.html',user=user)
    return wrapper