from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
import requests
from .models import Todo
from . import auth

main = Blueprint('main', name)

@main.route('/')
def index():
    # Redirect to the login page
    return redirect(url_for('auth.login'))

@main.route('/profile')
@login_required
def profile():
    user_name = current_user.name
    user_todos = Todo.query.filter_by(user_id=current_user.id).all()
    api_data = get_jsonplaceholder_data(current_user.id)  # Fetch user-specific API data
    return render_template('profile.html', name=user_name, user_todos=user_todos, api_data=api_data)

@main.route('/api/users', methods=['GET'])
@login_required
def api_users():
    # Secure API endpoint with login_required decorator
    user_id = current_user.id
    api_data = get_jsonplaceholder_data(user_id)  # Fetch user-specific API data
    if api_data is not None:
        return jsonify(api_data), 200
    else:
        return jsonify({'error': 'Failed to fetch data from API'}), 500

def get_jsonplaceholder_data(user_id):
    # Fetch todos specific to the user from JSONPlaceholder
    url = f'https://jsonplaceholder.typicode.com/todos?userId={user_id}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None