import sys
import os

# Thêm đường dẫn của thư mục chứa ứng dụng vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from website import db, create_app
from website.backend.models import Product

app = create_app()
# Thiết lập ngữ cảnh ứng dụng
with app.app_context():
    # Tạo dữ liệu mới cho đồ dùng học tập
    product1 = Product(name="Notebook", price=2.50, description="A 100-page ruled notebook", picture="notebook.jpg")
    product2 = Product(name="Pen", price=1.00, description="A blue ink ballpoint pen", picture="pen.jpg")
    product3 = Product(name="Pencil", price=0.50, description="A HB graphite pencil", picture="pencil.jpg")
    product4 = Product(name="Eraser", price=0.20, description="A white eraser", picture="eraser.jpg")
    product5 = Product(name="Ruler", price=1.25, description="A 30 cm plastic ruler", picture="ruler.jpg")

    # Thêm dữ liệu vào session
    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)
    db.session.add(product4)
    db.session.add(product5)

    # Lưu dữ liệu vào database
    db.session.commit()

    print("Data has been added to the Product table.")