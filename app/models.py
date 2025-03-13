from datetime import date
from . import  db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    hashed_password = db.Column(db.String(100), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")
    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    books = db.relationship('Book', backref='author', lazy=True)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    publish_date = db.Column(db.Date, nullable=False, default=date.today) 
    price = db.Column(db.Float, nullable=False)
    appropriate_for = db.Column(db.String(20), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False,)
