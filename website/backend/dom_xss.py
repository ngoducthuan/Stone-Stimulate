import os
from flask import Blueprint, Response, current_app, jsonify, redirect, render_template, request, send_file, url_for
from flask_login import login_user, login_required, logout_user, current_user # type: ignore
import requests
from website import db
import sqlite3
from datetime import datetime, timezone

dom_xss = Blueprint('dom_xss', __name__)
@dom_xss.route('/dom-xss/home')
@login_required
def home_product():
    #db_path = os.path.join(current_app.instance_path, 'stone.db')
    conn = sqlite3.connect('instance/stone.db')
    cursor = conn.cursor()
    query = "SELECT * FROM product"
    cursor.execute(query)
    products = cursor.fetchall()
    conn.close()
    print(products)

    # Chuyển đổi tuple thành dictionary
    products = [{'id': row[0], 'name': row[1], 'price': row[2], 'description': row[3], 'picture': row[4], 'rating': row[5]} for row in products]

    return render_template('dom-xss.html', products=products, user=current_user)