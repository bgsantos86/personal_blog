import json
import datetime
import logging

from flask import (Flask, render_template, request, jsonify, Response)
from peewee import *
from playhouse.shortcuts import model_to_dict

# App configuration
app = Flask(__name__)
db = SqliteDatabase('blog.db')
logging.basicConfig(filename='blog.log', level=logging.DEBUG)

# Modelo - Post
class Post(Model):
    title = CharField(max_length=255)
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

# Inicia o banco e dados e cria a tabela
def initialize():
    '''Create table 'Post' if they not exists. '''
    db.create_tables([Post], safe=True)

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

# Raiz da aplicação
@app.route('/', methods=['GET'])
def index():
    return jsonify({ 'msg': '404 Error - Path não mapeado!' })

# Criar post no banco de dados
@app.route('/post', methods=['POST'])
def add_post():
    title = request.json['title']
    content = request.json['content']
    post = Post.create(title=title, content=content)
    json_data = json.dumps(model_to_dict(post), default=str)
    logging.debug(json_data)
    return json_data

# Retorna lista de post
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.select().order_by(Post.timestamp.desc())
    array_posts = []
    json_response = {'lista': array_posts}

    for post in posts:
        json_data = json.dumps(model_to_dict(post), default=str)
        array_posts.append(json_data)
    logging.debug(json_response)

    response = Response(json.dumps(json_response, default=str), status=200, mimetype='application/json')
    logging.debug(response)
    return response

# Busca um post por id e retorna
@app.route('/post/<postid>', methods=['GET'])
def get_post(postid):
    try:
        post = Post.get_by_id(int(postid))
        json_data = json.dumps(model_to_dict(post), default=str)
        logging.debug(json_data)
        response = Response(json_data, status=200, mimetype='application/json')
        return response
    except:
        return not_found()


@app.before_request
def before_request():
    db.connect()

if __name__ == '__main__':
    initialize()
    app.run(debug=True, host='0.0.0.0', port=8080)