import json
import os
import platform
import socket
import time
from flask import Flask, jsonify, render_template_string
from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

START_TIME = time.time()

app = Flask(__name__)

app.secret_key = 'super_secret_session_key'  # Protects session cookies

# In-memory database simulation for this exercise
USER_DATABASE = {}

def load_config(path='config.json'):
	with open(path, 'r') as f:
		return json.load(f)

@app.get('/api/health')
def health():
	return jsonify({'status':'ok'})

@app.get('/api/config')
def config():
	return jsonify(load_config())

@app.get('/')
def home():
	cfg = load_config()
	html = (
	    '<h1>{{ name }}</h1>'
	    '<p>Version: {{ ver }}</p>'
	    '<p><a href="/api/health">/api/health</a></p>'
	)
	return render_template_string(
	    html,
	    name=cfg['app_name'],
	    ver=cfg['version']
	)

@app.get('/api/report')
def report():
	return jsonify({
	    'hostname': socket.gethostname(),
	    'python_version': platform.python_version(),
	    'uptime_seconds': round(time.time() - START_TIME, 2)
	})

### NEW FEATURE - AUTHENTICATION ###

# Decorator to protect sensitive backend routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({"error": "Unauthorized access. Login required."}), 401
        return f(*args, **kwargs)
    return decorated_function

# 1. Registration Endpoint
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    if username in USER_DATABASE:
        return jsonify({"error": "User already exists"}), 400
        
    # Securely hash the password before saving
    USER_DATABASE[username] = generate_password_hash(password)
    return jsonify({"message": f"User {username} registered successfully"}), 201

# 2. Login Endpoint
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    
    hashed_password = USER_DATABASE.get(username)
    if not hashed_password or not check_password_hash(hashed_password, password):
        return jsonify({"error": "Invalid username or password"}), 401
        
    # Issue a secure session cookie
    session['user'] = username
    return jsonify({"message": "Login successful"}), 200

# 3. Protected Dashboard Endpoint (Requires login decorator)
@app.route('/api/dashboard', methods=['GET'])
@login_required
def dashboard():
    return jsonify({"message": f"Welcome to your private dashboard, {session['user']}!"}), 200

### END OF NEW FEATURE - AUTHENTICATION ###

if __name__ == '__main__':
	app.run(
	    host='0.0.0.0',
	    port=int(os.environ.get('PORT', 8080)),
	    debug=True
	)
