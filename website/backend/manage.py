from datetime import date
import os
from flask import Blueprint, app, flash, jsonify, redirect, render_template, url_for, request

from . import views
from .models import User
from flask_login import login_user, login_required, logout_user, current_user 
from .models import User, Note
from website import db
import json
import sqlite3
from werkzeug.utils import secure_filename
from flask import current_app


# Define allowed_file inside create_app
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

manage = Blueprint('manage', __name__)

@manage.route('/user', methods=['GET','POST'])
@login_required
def user_page():
    user_info = {
        "firstName": current_user.firstName,
        "lastName": current_user.lastName,
        "email": current_user.email,
        "avatar_url": '',
    }
    
    if request.method == 'POST':
        # Handle file upload
        if 'avatar' not in request.files:
            flash('No file part',category='error')
            return redirect(request.url)
        file = request.files['avatar']
        if file.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("Oke")
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            print(file_path)
            file.save(file_path)
            # Update user's avatar URL in your database
            user_info['avatar_url'] = url_for('static', filename=f'uploads/{filename}')

            # Create url link
            avatar_url = url_for('static', filename=f'uploads/{filename}')
            #print(avatar_url)
            # Update the user's avatar_url in the database
            current_user.avatar_url = avatar_url
            db.session.commit()

            print(user_info)
            #update_user_avatar(username, user_info['avatar_url'])
            flash('Avatar updated successfully')
            return redirect(request.url)

    return render_template('user.html', user=current_user)
@manage.route('/admin')
@login_required # If don't have. We can access admin page without login
def admin_page():
    #YOu must cheeck account wheather it is admin account. If you not check, everything user logged can access this page
    if current_user.email == 'admin@gmail.com':
        conn = sqlite3.connect('instance/stone.db')
        cursor = conn.cursor()
        query = f"SELECT * from user"
        cursor.execute(query)
        users = cursor.fetchall()
        #print(users)
        conn.close()

        return render_template('admin.html', user=current_user, users=users)
    else:
        flash("You can access admin page!", category='error')
        return redirect(url_for('views.home'))

@manage.route('/delete-user', methods=['POST'])
@login_required # If don't have. We can access admin page without login
def delete_user():
    user_data = json.loads(request.data)
    userEmail = user_data.get('userEmail')
    print(userEmail)
    user = User.query.filter_by(email=userEmail).first()
    user_id = user.id
    # if note:
    #     if note.user_id == current_user.id:
    #         db.session.delete(note)
    #         db.session.commit()
    #         flash("Deleted Successfully!", category='success')
    print(user.email)
    db.session.delete(user)
    db.session.commit()
    flash("Deleted Successfully!", category='success')
    return jsonify({})
