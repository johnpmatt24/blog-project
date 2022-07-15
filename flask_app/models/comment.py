from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# model the class after the friend table from our database
class Comment:
    def __init__( self , data ):
        self.id = data['id']
        self.content = data["content"]
        self.writer_first_name = data["writer_first_name"]
        self.writer_last_name = data["writer_last_name"]
        self.user_id = data["user_id"]
        self.post_id = data["post_id"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * from comments;"
        results = connectToMySQL('paa').query_db(query)
        # Create an empty list to append our instances
        comments = []
        # Iterate over the db results and create instances
        for comment in results:
            comments.append( cls(comment) )
        return comments
    
    
    @classmethod
    def get_comment(cls, data):
        query = "SELECT users.first_name as writer_first_name, users.last_name as writer_last_name, comments.* from comments left join users on users.id = comments.user_id where comments.id = %(id)s;"
        results = connectToMySQL('paa').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    
    @classmethod
    def get_posts_comments(cls, data):
        query = "SELECT users.first_name as writer_first_name, users.last_name as writer_last_name, comments.* from comments left join users on users.id = comments.user_id where post_id = %(post_id)s;"
        results = connectToMySQL('paa').query_db(query, data)
        # Create an empty list to append our instances
        comments = []
        # Iterate over the db results and create instances
        for comment in results:
            comments.append( cls(comment) )
        return comments
    
    
    
    @classmethod
    def add_comment(cls, data):
        query = "INSERT INTO comments (content, user_id, post_id, created_at, updated_at) VALUES (%(content)s, %(user_id)s, %(post_id)s , NOW(), NOW());" # this returns an id
        return connectToMySQL('paa').query_db(query, data)
    
    
    @classmethod
    def update_comment(cls, data):
        query = "UPDATE comments SET content = %(content)s, created_at = NOW(), updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('paa').query_db(query, data)
    
    
    
    @classmethod
    def delete_comment(cls, data):
        query = "DELETE from comments where id = %(id)s and post_id = %(post_id)s;"
        return connectToMySQL('paa').query_db(query, data)
    
    
    @classmethod
    def delete_post_comments(cls, data):
        query = "DELETE from comments where post_id = %(post_id)s;"
        return connectToMySQL('paa').query_db(query, data)
    
    
    
    @staticmethod
    def is_valid(comment):
        is_valid = True # we assume this is true
        if len(comment['content']) <= 0:
            flash("No comment was entered")
            is_valid = False
        return is_valid