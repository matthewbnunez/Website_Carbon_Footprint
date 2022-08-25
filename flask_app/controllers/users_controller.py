from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.URL_model import URL


bcrypt = Bcrypt(app)

# bcrypt.generate_password_hash(password_string)
# bcrypt.check_password_hash(hashed_password, password_string)


@app.route('/')
def RegisterAndLogin():
    if "user_id" in session:
        return redirect('/welcome')
    return render_template('register_and_login.html')


# display welcome page
@app.route('/welcome')
def welcome():
    if not 'user_id' in session:
        return redirect('/')
    user = User.get_by_id({'id': session['user_id']})
    all_urls = URL.get_all()
    return render_template('dashboard.html', user = user, all_urls = all_urls)


# Logout user
@app.route('/users/logout')
def logout():
    del session['user_id']
    return redirect('/')


# Register a new user
@app.route('/users/register', methods=['POST']) #action route
def RegisterUser():
    if not User.validate(request.form):
        return redirect('/')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashed_pw
    }
    session['user_id'] = User.create_user(data)
    return redirect('/')


# Login user
@app.route('/users/login', methods=["POST"])
def login():
    data = {
        'email': request.form['email']
    }
    user_from_db = User.get_by_email(data)
    if not user_from_db:
        flash("Invaild Credentials", "log")
        return redirect('/')
    if not bcrypt.check_password_hash(user_from_db.password, request.form['password']):
        flash("Invaild Credentials", "log")
        return redirect('/')
    session['user_id'] = user_from_db.id
    return redirect('/')
