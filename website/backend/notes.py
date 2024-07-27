from datetime import date
from flask import Blueprint, flash, jsonify, redirect, render_template, url_for, request

from . import views
from .models import User
from flask_login import login_user, login_required, logout_user, current_user 
from .models import User
from .models import Note
from website import db
import json
import sqlite3
note = Blueprint('note', __name__)

@note.route('/notes', methods=['GET', 'POST'])
@login_required
def note_page():
    if request.method == 'POST':
        note = request.form.get('note')
        print(note)
        if(len(note) < 1):
            flash("Note is too short!", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            conn = sqlite3.connect('instance/stone.db')
            cursor = conn.cursor()
            # Example of updating a table based on the new_note object
            query = f"INSERT INTO note (data, user_id) VALUES ('{new_note.data}', '{new_note.user_id}')"
            # Exploit
            # insert into note (data, user_id) values ('a','1') union SELECT CONCAT(email, ':', password) AS email_and_password, 1 AS constant_value FROM user;
            cursor.execute(query)

            # Committing the transaction
            conn.commit()
            # Closing the connection
            conn.close()
            #db.session.add(new_note)
            #db.session.commit()
            flash("Note added!", category='success')
    return render_template('note.html', user=current_user)
@note.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Deleted Successfully!", category='success')
    return jsonify({})

