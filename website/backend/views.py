import os
import subprocess
from flask import Blueprint, Response, jsonify, redirect, render_template, request, send_file, url_for
from flask_login import login_user, login_required, logout_user, current_user # type: ignore
import requests

views = Blueprint('views', __name__)
products = [
    {'id': 1, 'name': 'Product 1', 'price': 100000, 'description': 'Mô tả sản phẩm 1', 'picture': 'p1.jpg'},
    {'id': 2, 'name': 'Product 2', 'price': 150000, 'description': 'Mô tả sản phẩm 2', 'picture': 'p2.jpg'},
    {'id': 3, 'name': 'Product 3', 'price': 120000, 'description': 'Mô tả sản phẩm 3', 'picture': 'p3.jpg'}
]
@views.route('/')
@login_required
def home():
    return render_template("home.html",user=current_user, products=products)
@views.route('/image')
def request_file():
    filename = request.args.get('filename')
    if not filename:
        return 'Missing filename parameter', 400
    filepath = os.path.join('/home/kali/Downloads/Stone/website/static/img', filename)
    if not os.path.exists(filepath):
        print("Oke")
        return 'File not found', 404
    return send_file(filepath)

@views.route('/product?productId=<int:productId>')
@login_required
def request_product(productId):
    # Tìm sản phẩm có id tương ứng trong danh sách
    product = next((p for p in products if p['id'] == productId), None)
    if product:
        return render_template('product.html', product=product, user=current_user)
    else:
        return 'Sản phẩm không tồn tại.'


FILES_DIR = '/home/kali/Downloads/Stone/website/static/list_files'
@views.route('/files', methods=['GET', 'POST'])
@login_required
def read_file():
    file_content = ''
    if request.method == 'POST':
        file_name = request.form.get('file_name')
        print(file_name)
        try:
            # Command injection trong lệnh `cat` để đọc file
            command = f"cat {FILES_DIR}/{file_name}"
            print(command)
            output = subprocess.run(command, shell=True, capture_output=True, text=True)
            file_content = output.stdout
            print(file_content)
        except Exception as e:
            file_content = str(e)
    
    return render_template('file_content.html', file_content=file_content, user=current_user)

VIRUSTOTAL_API_KEY = 'e47339e1b300c7503b8eb41df457f79e8054a17ee8d2cf3f7facf14b784199b1'
@views.route('/check_hash', methods=['GET', 'POST'])
@login_required
def check_file():
    result = None
    full_url = None
    if request.method == 'POST':
        full_url = request.form.get('full_url')
        print(full_url)
        headers = {
            'x-apikey': VIRUSTOTAL_API_KEY
        }
        try:
            response = requests.get(full_url, headers=headers)
            print(response)
            if response.status_code == 200:
                return response.text
            else:
                result = {'error': 'Unable to fetch data'}
        except requests.RequestException as e:
            result = {'error': str(e)}
        #return jsonify(result=result, full_url=full_url)
    return render_template('check_hash.html', user=current_user)
    
@views.route('/xss-stimulate', methods=['GET', 'POST'])
@login_required
def search_product():
    query = request.args.get('query', '')
    filtered_products = [p for p in products if query.lower() in p['name'].lower()]
    response = f"<p></p>"
    if query:
        response = f"<p><strong>You searched for</strong>: {query}</p>"
    return render_template('xss-stimulate.html', products=filtered_products, response=response, user=current_user)