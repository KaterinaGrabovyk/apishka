from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from database import db
from sqlalchemy.orm import relationship

class Customer(db):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    rented_books = relationship('RentedBook', back_populates='customer', cascade='all, delete-orphan')


class RentedBook(db):
    __tablename__ = 'rented_books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False) 
    rent_date = Column(Date, nullable=False)  
    return_date = Column(Date, nullable=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)  
    customer = relationship('Customer', back_populates='rented_books')
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)