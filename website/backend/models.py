from datetime import datetime
from website import db
from flask_login import UserMixin, current_user # type: ignore
from sqlalchemy.sql import func # type: ignore
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, data, user_id):
        self.data = data
        self.user_id = user_id    
    
    def __repr__(self):
        return f"<Note {self.id}>"
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    avatar_url = db.Column(db.String(255))
    notes = db.relationship('Note')
    
    def __init__(self, email, password, firstName, lastName, id=None, avatar_url=None):
        self.id = id
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.avatar_url = avatar_url

    def __repr__(self):
        return f"<User {self.id}>"
    
# class Controller(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated
#     def not_auth(self):
#         return "You are not authorized to use the admin dasboard."
        
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    picture = db.Column(db.String(200), nullable=True)

    def __init__(self, name, price, description, picture, id=None):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.picture = picture
        
    def __repr__(self):
        return f"<Product {self.id}>"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Product', backref=db.backref('comments', lazy=True))

    def __init__(self, product_id, name, comment, rating, created_at, id=None):
        self.id = id
        self.product_id = product_id
        self.name = name
        self.comment = comment
        self.rating = rating
        self.created_at = created_at

    def __repr__(self):
        return f"<Comment {self.id}>"