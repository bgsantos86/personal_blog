from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('blog.db')

class Post(Model):
    # (unique) id
    # title
    # content
    title = CharField(max_length=255)
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def initialize():
    '''Create table 'Post' if they not exists. '''
    db.connect()
    db.create_tables([Post], safe=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_loop():
    ''' Show menu '''
    choice = None

    while choice != 'q':
        clear()
        print("Digite 'q' para sair!")
        for key, value in menu.items():
            print(f"{key}) {value.__doc__}")
        choice = input('Ação ').lower().strip()

        if choice in menu:
            menu[choice]()

def add_post():
    ''' Add a post. '''
    clear()
    print("Digite o titulo do post: (crtl+d para terminal)")
    data_title = sys.stdin.read().strip()
    clear()

    print("\nDigite o conteúdo do post: (crtl+d para terminal)")
    data_content = sys.stdin.read().strip()

    if data_title and data_content:
        if input('\nSalvar entrada? [Sn] ').lower() != 'n':
            Post.create(title=data_title, content=data_content)
            print('Salvo com sucesso!')

def view_posts():
    ''' View previues posts '''
    clear()
    posts = Post.select().order_by(Post.timestamp.desc())
    
    for post in posts:
        timestamp = post.timestamp.strftime('%A %B %d, %Y %H:%M')
        print(timestamp)
        print('='*len(timestamp))
        print(post.title)
        print('='*len(timestamp))
        print(post.content)
        print('='*len(timestamp))
        
        print('\nn) next entry')
        print('d) delete entry')
        print('r) return to menu!\n')

        next_action = input('Action: [Ndr] ').lower().strip()
        print()
        if next_action == 'r':
            break
        elif next_action == 'd':
            pass
            #TODO: chamar função para deletar arquivo

menu = OrderedDict([
    ('a', add_post),
    ('v', view_posts)
])

if __name__ == '__main__':
    initialize()
    menu_loop()