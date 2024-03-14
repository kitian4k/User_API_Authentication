# In api.py
from flask import Blueprint, jsonify
from flask_httpauth import HTTPBasicAuth
from .models import Todo, User
import requests

api = Blueprint('api', __name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user

@api.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    user = auth.current_user()
    todos = get_jsonplaceholder_data(user.id)
    return jsonify({'todos': todos})

def get_jsonplaceholder_data(user_id):
    url = f'https://jsonplaceholder.typicode.com/todos?userId={user_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
