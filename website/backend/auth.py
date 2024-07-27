from flask import Blueprint, flash, redirect, render_template, url_for, request

from . import views

from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
import sqlite3
from flask_login import login_user, login_required, logout_user, current_user 
from functools import wraps

auth = Blueprint('auth', __name__)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        #user1 = User.query.filter_by(email=email).first()
        #print(user1)
        # if user:
        #     if  check_password_hash(user.password, password):
        #         flash('Logged in successfully!', category='success')
        #         return render_template('user.html')
        #     else:
        #         flash('Incorrect password, try again.', category='error')
        # else:
        #     flash('Email does not exist!', category='error')
        
    
        conn = sqlite3.connect('instance/stone.db')
        cursor = conn.cursor()
        print(cursor)
        """
        # Login patterm 1
        # Tạo câu lệnh SQL trực tiếp với tham số từ người dùng
        query = f"SELECT * FROM user WHERE email = '{email}'"
        cursor.execute(query)

        user_row = cursor.fetchone()
        print(user_row)
        conn.close()
        if user_row:
            user = User(user_row[0], user_row[1], user_row[2], user_row[3], user_row[4])
            # Kiểm tra mật khẩus   
            print(user)
            if  check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            return "User not found."
        """

        query = f"SELECT * from user WHERE email = '{email}' AND password = '{password}'"
        cursor.execute(query)
        user_row = cursor.fetchone()
        print(user_row)
        conn.close()
        if user_row:
            #Check admin account
            user = User(user_row[1], user_row[2], user_row[3], user_row[4], user_row[0])
            print(user)
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            if user.email == 'admin@gmail.com':   
                resp = redirect(url_for('views.home'))
                return resp
            else:
                resp = redirect(url_for('views.home'))
                return resp
        else:
            flash('Incorrect password, try again.', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    #Add informatin form user request
    if(request.method == 'POST'):
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password = request.form.get('password1')
        confirm_password = request.form.get('password2')
    
        #Check data and Add information to database
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email alreaddy exists', category='error')
        elif len(email) <= 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password != confirm_password:
            flash('Password don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            #Add new user
            new_user = User(email=email, firstName=firstName, lastName=lastName, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            #Alert
            flash('Account is created!', category='success')
            return redirect(url_for('views.home'))
            #return render_template('login.html', user=current_user)
    return render_template('sign-up.html', user=current_user)


