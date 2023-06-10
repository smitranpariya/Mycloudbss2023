
import bcrypt
from flask import app, redirect,request,jsonify,render_template, url_for,session
from flask_pymongo import PyMongo
from main import mongo


def do_signup():
    message = ''
    db = mongo.db
    if request.method == "POST":
        user = request.form.get("username")
        email = request.form.get("email")
        
        password1 = request.form.get("password")
        password2 = request.form.get("confirm_password")
        
        user_found = db.admins.find_one({"name": user})
        email_found = db.admins.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('signup_page.html', message=message)
        if email_found:
            message = 'This email already exists!'
            return render_template('signup_page.html', message=message)
        if password1 != password2:
            message = "Passwords shouldn't match!"
            return render_template('signup_page.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'username': user, 'email': email, 'password': hashed}
            db.admins.insert_one(user_input)
            
            user_data = db.admins.find_one({"email": email})
            new_email = user_data['email']
            return redirect(url_for("ret_login"))
        



