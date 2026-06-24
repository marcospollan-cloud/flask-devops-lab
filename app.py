import json
import os
import platform
import socket
import time
from flask import Flask, jsonify, render_template_string

START_TIME = time.time()

app = Flask(__name__)

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

if __name__ == '__main__':
	app.run(
	    host='0.0.0.0',
	    port=int(os.environ.get('PORT', 8080)),
	    debug=True
	)
