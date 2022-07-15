from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 


class Post:
    def __init__(self, data):
        self.pid = data['pid']
        self.creator_first_name = data["creator_first_name"]
        self.creator_last_name = data["creator_last_name"]
        self.image_name = data["image_name"]
        self.title = data["title"]
        self.content = data['content']
        self.user_id = data["user_id"]
        self.image_id = data["image_id"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 
        
        
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('paa').query_db(query)
        # Create an empty list to append our instances
        posts = []
        # Iterate over the db results and create instances
        for post in results:
            posts.append( cls(post) )
        return posts
    
    
    
    
    @classmethod
    def get_all_post_with_users(cls):
        query = "SELECT users.first_name as creator_first_name, users.last_name as creator_last_name, images.file as image_name, posts.* from posts left join users on users.id = posts.user_id left join images on images.id = posts.image_id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('paa').query_db(query)
        # Create an empty list to append our instances
        posts = []
        # Iterate over the db results and create instances
        for post in results:
            posts.append( cls(post) )
        return posts
    
    
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO posts ( title, content, user_id, image_id, created_at, updated_at ) VALUES ( %(title)s, %(content)s , %(user_id)s, %(image_id)s, NOW() , NOW() );" # will return id can also be called create
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('paa').query_db( query, data ) 
    
    
    
    @classmethod
    def get_post(cls, data):
        query = "SELECT users.first_name as creator_first_name, users.last_name as creator_last_name, images.file as image_name, posts.* from posts left join users on users.id = posts.user_id left join images on images.id = posts.image_id where pid = %(pid)s";
        results = connectToMySQL('paa').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    
    
    @classmethod
    def get_user_posts(cls, data):
        query = "SELECT * from posts where user_id = %(user_id);"
        results = connectToMySQL('paa').query_db(query, data)
        posts = []
        
        for post in results:
            posts.append( cls(post) )
        return posts
    
    
    
    
    @classmethod
    def update_post(cls, data):
        query = "UPDATE posts SET title = %(title)s, content = %(content)s, created_at = NOW(), updated_at = NOW() WHERE pid = %(pid)s;"
        return connectToMySQL('paa').query_db(query, data)
    
    
    @classmethod
    def delete_post(cls, data):
        query = "DELETE from posts where pid = %(pid)s;"
        return connectToMySQL('paa').query_db(query, data)
    
    
    
    @staticmethod
    def is_valid(post):
        is_valid = True # we assume this is true
        if len(post['title']) <= 0:
            flash("Please enter a title.")
            is_valid = False
        if len(post['content']) <= 0:
            flash("Say something about the game.")
            is_valid = False
        return is_valid