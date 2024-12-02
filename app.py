from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt
)
from config import Config
from database import db, migrate
import crud

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
jwt = JWTManager(app)
#tokens
revoked_tokens = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in revoked_tokens

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        user = crud.create_user(username, password)
        if user is None:
            return jsonify({"error": "User already exists"}), 400

        return jsonify({"message": "User registered successfully"}), 201
    except Exception:
        return jsonify({"error": "An error occurred during registration"}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = crud.get_user_by_username(username)
        if user is None or not user.check_password(password):
            return jsonify({"error": "Invalid username or password"}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    except Exception:
        return jsonify({"error": "An error occurred during login"}), 500


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        revoked_tokens.add(jti)
        return jsonify({"message": "Token revoked"}), 200
    except Exception:
        return jsonify({"error": "An error occurred during logout"}), 500


@app.route('/customers', methods=['POST'])
@jwt_required()
def add_customer():
    try:
        data = request.get_json()
        customer = crud.create_customer(data['name'], data['email'], data.get('phone'))
        return jsonify({"id": customer.id, "name": customer.name, "email": customer.email, "phone": customer.phone})
    except Exception:
        return jsonify({"error": "An error occurred while adding the customer"}), 500


@app.route('/customers/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_customer(customer_id):
    try:
        customer = crud.get_customer_by_id(customer_id)
        if customer:
            return jsonify({"id": customer.id, "name": customer.name, "email": customer.email, "phone": customer.phone})
        return jsonify({"error": "Customer not found"}), 404
    except Exception:
        return jsonify({"error": "An error occurred while retrieving the customer"}), 500


@app.route('/customers', methods=['GET'])
@jwt_required()
def get_all_customers():
    try:
        customers = crud.get_all_customers()
        return jsonify([{"id": customer.id, "name": customer.name, "email": customer.email, "phone": customer.phone} for customer in customers])
    except Exception:
        return jsonify({"error": "An error occurred while retrieving customers"}), 500


@app.route('/rented_books', methods=['POST'])
@jwt_required()
def add_rented_book():
    try:
        data = request.get_json()
        rented_book = crud.create_rented_book(
            data['title'], data['rent_date'], data['customer_id'], data.get('return_date')
        )
        return jsonify({
            "id": rented_book.id,
            "title": rented_book.title,
            "rent_date": str(rented_book.rent_date),
            "return_date": str(rented_book.return_date) if rented_book.return_date else None,
            "customer_id": rented_book.customer_id
        })
    except Exception:
        return jsonify({"error": "An error occurred while adding the rented book"}), 500


@app.route('/rented_books/<int:book_id>', methods=['GET'])
@jwt_required()
def get_rented_book(book_id):
    try:
        rented_book = crud.get_rented_book_by_id(book_id)
        if rented_book:
            return jsonify({
                "id": rented_book.id,
                "title": rented_book.title,
                "rent_date": str(rented_book.rent_date),
                "return_date": str(rented_book.return_date) if rented_book.return_date else None,
                "customer_id": rented_book.customer_id
            })
        return jsonify({"error": "Rented book not found"}), 404
    except Exception:
        return jsonify({"error": "An error occurred while retrieving the rented book"}), 500


@app.route('/rented_books', methods=['GET'])
@jwt_required()
def get_all_rented_books():
    try:
        rented_books = crud.get_all_rented_books()
        return jsonify([{
            "id": book.id,
            "title": book.title,
            "rent_date": str(book.rent_date),
            "return_date": str(book.return_date) if book.return_date else None,
            "customer_id": book.customer_id
        } for book in rented_books])
    except Exception:
        return jsonify({"error": "An error occurred while retrieving rented books"}), 500


@app.route('/rented_books/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_rented_book(book_id):
    try:
        data = request.get_json()
        rented_book = crud.update_rented_book(
            book_id,
            data.get('title'),
            data.get('rent_date'),
            data.get('return_date'),
            data.get('customer_id')
        )
        if rented_book:
            return jsonify({
                "id": rented_book.id,
                "title": rented_book.title,
                "rent_date": str(rented_book.rent_date),
                "return_date": str(rented_book.return_date) if rented_book.return_date else None,
                "customer_id": rented_book.customer_id
            })
        return jsonify({"error": "Rented book not found"}), 404
    except Exception:
        return jsonify({"error": "An error occurred while updating the rented book"}), 500


@app.route('/rented_books/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_rented_book(book_id):
    try:
        rented_book = crud.delete_rented_book(book_id)
        if rented_book:
            return jsonify({"message": "Rented book deleted"})
        return jsonify({"error": "Rented book not found"}), 404
    except Exception:
        return jsonify({"error": "An error occurred while deleting the rented book"}), 500

if __name__ == '__main__':
    app.run(debug=True)