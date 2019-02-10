from run import app
from flask import jsonify


@app.route('/')
def index():
    return jsonify({'message': 'This is an authorization microservice by cookie army!'})
