import json
import datetime

from flask import (Flask, render_template, request, jsonify)
from peewee import *

# App configuration
app = Flask(__name__)
db = SqliteDatabase('blog.db')

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
    db.connect()
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
    return jsonify({'id': post.id})

@app.before_request
def before_request():
    db.connect()

if __name__ == '__main__':
    initialize()
    app.run(debug=True, host='0.0.0.0', port=8080)