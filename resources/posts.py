from flask import jsonify, Blueprint
from flask_restful import   (Resource, Api, reqparse, fields,
                            marshal, marshal_with, abort, url_for)

import models

post_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'timestamp': fields.DateTime
}

def post_or_404(post_id):
    try:
        post = models.Post.get(models.Post.id==post_id)
    except models.Post.DoesNotExist:
        abort(404, message='Post {} does not exist'.format(post_id))
    else:
        return post

class PostList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=True,
            help='No post title provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'content',
            required=False,
            nullable=True,
            help='No post content provided',
            location=['form', 'json'],
            default=''
        )
        super().__init__()

    def get(self):
        posts = [marshal(post, post_fields)
                for post in models.Post.select()]
        return {'posts': posts}

    @marshal_with(post_fields)
    def post(self):
        args = self.reqparse.parse_args()
        post = models.Post.create(**args)
        return (post, 201, 
                {'Location': url_for('resources.posts.posts')})

class Post(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=True,
            help='No post title provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'content',
            required=False,
            nullable=True,
            help='No post content provided',
            location=['form', 'json'],
            default=''
        )
        super().__init__()

    @marshal_with(post_fields)
    def get(self, id):
        return post_or_404(id)

    @marshal_with(post_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Post.update(**args).where(models.Post.id == id)
        query.execute()
        return (post_or_404(id), 200, 
                {'Location': url_for('resources.posts.post', id=id)})

    def delete(self, id):
        query = models.Post.delete().where(models.Post.id == id)
        query.execute()
        return ('', 204, 
                {'Location': url_for('resources.posts.posts')})

posts_api = Blueprint('resources.posts', __name__)
api = Api(posts_api)
api.add_resource(
    PostList,
    '/api/v1/posts',
    endpoint='posts'
)
api.add_resource(
    Post,
    '/api/v1/posts/<int:id>',
    endpoint='post'
)