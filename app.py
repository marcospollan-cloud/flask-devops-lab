import json
import os
from flask import Flask, jsonify, render_template_string

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
	cfg = load-config()
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

if __name__ == '__main__':
	app.run(
	    host='0.0.0.0',
	    port=int(os.environ.get('PORT', 8080)),
	    debug=True
	)
