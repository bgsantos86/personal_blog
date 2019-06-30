from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('blog.db')

class Post(Model):
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

def add_post(update=False, post=None):
    ''' Add a post. '''
    clear()
    print("Digite o titulo do post: (crtl+d para terminal)")
    data_title = sys.stdin.read().strip()
    clear()

    print("Digite o conteúdo do post: (crtl+d para terminal)")
    data_content = sys.stdin.read().strip()
    clear()

    if data_title and data_content:
        if input('Salvar entrada? [Sn] ').lower() != 'n':
            if update and post:
                #Post.insert(title=data_title, content=data_content).on_conflict('replace').execute()
                post.title = data_title
                post.content = data_content
                post.save()
            else:
                Post.create(title=data_title, content=data_content)
                print('Salvo com sucesso!')

def view_posts(search_query=None, search_attr='title'):
    ''' View previues posts '''
    posts = Post.select().order_by(Post.timestamp.desc())

    if search_query and search_attr == 'title':
        posts = posts.where(Post.title.contains(search_query))
    elif search_query and search_attr == 'content':
        posts = posts.where(Post.content.contains(search_query))
    
    for post in posts:
        clear()
        timestamp = post.timestamp.strftime('%A %B %d, %Y %H:%M')
        print(timestamp)
        print('='*len(timestamp))
        print(post.title)
        print('='*len(timestamp))
        print(post.content)
        print('='*len(timestamp))
        
        print('\nn) next entry')
        print('d) delete entry')
        print('u) update entry')
        print('r) return to menu!\n')

        next_action = input('Action: [Ndr] ').lower().strip()
        clear()
        if next_action == 'r':
            break
        elif next_action == 'd':
            delete_post(post)
        elif next_action == 'u':
            update_post(post.id)

def delete_post(post):
    ''' Delete a post '''
    clear()
    if input("Are you sure? [yN] ").lower() == 'y':
        post.delete_instance()
        print('Post deleted!')

def search_in_title():
    ''' Search for a string in title '''
    view_posts( input('Search in title: ') )

def search_in_content():
    ''' Search for a string in content '''
    view_posts( view_posts( input('Search in content: '), 'content' ) )

def  search_by_id(id):
    ''' Search by an id. '''
    #post = Post.select().where(Post.id == id)
    post = Post.get_by_id(id)
    return post

def update_post(id):
    post = search_by_id(id)
    add_post(update=True, post=post)

menu = OrderedDict([
    ('a', add_post),
    ('v', view_posts),
    ('t', search_in_title),
    ('c', search_in_content)
])

if __name__ == '__main__':
    initialize()
    menu_loop()