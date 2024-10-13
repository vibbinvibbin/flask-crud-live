from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load environment variables
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}


# Create database tables
with app.app_context():
    db.create_all()


# Create a test route
@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)


# Create a user
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if 'username' not in data or 'email' not in data:
            return make_response(jsonify({'message': 'username and email are required'}), 400)

        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'user created', 'user': new_user.json()}), 201)
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return make_response(jsonify({'message': 'error creating user'}), 500)


# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]), 200)
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        return make_response(jsonify({'message': 'error getting users'}), 500)


# Get a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.get(id)
        if user:
            return make_response(jsonify({'user': user.json()}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        return make_response(jsonify({'message': 'error getting user'}), 500)


# Update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.get(id)
        if user:
            data = request.get_json()
            if 'username' not in data or 'email' not in data:
                return make_response(jsonify({'message': 'username and email are required'}), 400)

            user.username = data['username']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message': 'user updated', 'user': user.json()}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        return make_response(jsonify({'message': 'error updating user'}), 500)


# Delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'user deleted'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        return make_response(jsonify({'message': 'error deleting user'}), 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
