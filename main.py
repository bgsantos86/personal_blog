from flask import (Flask, render_template, request, jsonify, Response)

import models
from resources.posts import posts_api

# App configuration
DEBUG = True
HOST = '0.0.0.0'
PORT = 8080

app = Flask(__name__)
app.register_blueprint(posts_api)

# Raiz da aplicação
@app.route('/', methods=['GET'])
def index():
    return jsonify({ 'msg': 'Hello, blog!' })


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)