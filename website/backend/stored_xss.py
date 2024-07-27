import os
from flask import Blueprint, Response, current_app, jsonify, redirect, render_template, request, send_file, url_for
from flask_login import login_user, login_required, logout_user, current_user # type: ignore
import requests
from website import db
import sqlite3
from datetime import datetime, timezone

stored_xss = Blueprint('stored_xss', __name__)
@stored_xss.route('/stored-xss/home')
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

    return render_template('stored-xss.html', products=products, user=current_user)

@stored_xss.route('/stored-xss/product?id=<int:productId>', methods=['GET', 'POST'])
@login_required
def product_requested(productId):
    print('OKe')

    conn = sqlite3.connect('instance/stone.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        print('Get POST request oke.')
        # Handle comment submission
        comment = request.form.get('comment')
        user = current_user.lastName
        if comment:
            current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            print(type(current_time))
            query = 'INSERT INTO comment (product_id, name, comment, rating, created_at) VALUES (?, ?, ?, ?, ?)'
            cursor.execute(query, (productId, user, comment, 1, str(current_time)))
            conn.commit()
    #Get product information
    query = 'SELECT * FROM product WHERE id = ?'
    cursor.execute(query, (productId,))
    product = cursor.fetchone()
    #Get comment information
    query = 'SELECT * FROM comment WHERE product_id = ?'
    cursor.execute(query, (productId,))
    comments = cursor.fetchall()
    #Close connect
    conn.close()
    #Convet to dictionary
    product = {'id': product[0], 'name': product[1], 'price': product[2], 'description': product[3], 'picture': product[4], 'rating': product[5]}
    print(product)
    comments = [{'id': c[0], 'product_id': c[1], 'user': c[2], 'comment': c[3], 'rating':c[4], 'created_at': c[5]} for c in comments]
    print(comments)

    if product:
        return render_template('stored-xss-product-detailed.html', product=product, user=current_user, comments=comments)
    else:
        return 'Sản phẩm không tồn tại.'
    
# @stored_xss.route('/stored-xss/comment', methods=['GET', 'POST'])
# @login_required
# def submit_comment():
#     data = request.get_json()
#     comment = data.get('comment')
#     product_id = data.get('product_id')
#     user = data.get('username')
#     print("Get Oke")
    
#     if comment and product_id:
#         #Update comment to database
#         conn = sqlite3.connect('instance/stone.db')
#         cursor = conn.cursor()
#         query = 'INSERT INTO comment (product_id, name, comment, rating) VALUES (?, ?, ?, ?)'
#         cursor.execute(query, (product_id, user, comment, 0))
#         conn.commit()
#          # Fetch product details
#         query = 'SELECT * FROM product WHERE id = ?'
#         cursor.execute(query, (product_id,))
#         product = cursor.fetchone()
#         product = {'id': product[0], 'name': product[1], 'price': product[2], 'description': product[3], 'picture': product[4], 'rating': product[5]}
#         #Get data comment from database
#         query = 'SELECT * FROM comment WHERE product_id = ?'
#         cursor.execute(query, (product_id,))
#         comments = cursor.fetchall()
#         conn.close()
#         # Convert comments to a list of dictionaries
#         comments = [{'id': c[0], 'product_id': c[1], 'user': c[2], 'comment': c[3], 'rating':c[4], 'created_at': c[4]} for c in comments]
#         print(comments)
#         return render_template('stored-xss-product-detailed.html', product=product, comments=comments, user=current_user)
#     else:
#         return jsonify({'status': 'error', 'message': 'Missing comment or product_id.'}), 400