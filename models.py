import datetime

from peewee import *

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