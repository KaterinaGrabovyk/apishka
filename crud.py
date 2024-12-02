from database import db
from models import Customer, RentedBook
from models import User
def create_customer(name, email, phone=None):
    customer = Customer(name=name, email=email, phone=phone)
    db.session.add(customer)
    db.session.commit()
    return customer


def get_customer_by_id(customer_id):
    return Customer.query.get(customer_id)


def get_all_customers():
    return Customer.query.all()


def update_customer(customer_id, name=None, email=None, phone=None):
    customer = Customer.query.get(customer_id)
    if customer:
        if name:
            customer.name = name
        if email:
            customer.email = email
        if phone:
            customer.phone = phone
        db.session.commit()
    return customer


def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
    return customer


def create_rented_book(title, rent_date, customer_id, return_date=None):
    rented_book = RentedBook(
        title=title, 
        rent_date=rent_date, 
        return_date=return_date, 
        customer_id=customer_id
    )
    db.session.add(rented_book)
    db.session.commit()
    return rented_book


def get_rented_book_by_id(book_id):
    return RentedBook.query.get(book_id)


def get_all_rented_books():
    return RentedBook.query.all()


def update_rented_book(book_id, title=None, rent_date=None, return_date=None, customer_id=None):
    rented_book = RentedBook.query.get(book_id)
    if rented_book:
        if title:
            rented_book.title = title
        if rent_date:
            rented_book.rent_date = rent_date
        if return_date:
            rented_book.return_date = return_date
        if customer_id:
            rented_book.customer_id = customer_id
        db.session.commit()
    return rented_book


def delete_rented_book(book_id):
    rented_book = RentedBook.query.get(book_id)
    if rented_book:
        db.session.delete(rented_book)
        db.session.commit()
    return rented_book


def delete_customer_with_cascade(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
    return customer

def create_user(username, password):
    if User.query.filter_by(username=username).first():
        return None
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()