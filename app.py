import json
import datetime
import logging

from flask import (Flask, render_template, request, jsonify)
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
def list_all_posts():
    pass

@app.before_request
def before_request():
    db.connect()

if __name__ == '__main__':
    initialize()
    app.run(debug=True, host='0.0.0.0', port=8080)