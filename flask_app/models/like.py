from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
class Like:
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data["user_id"]
        self.post_id = data["post_id"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * from likes;"
        results = connectToMySQL('paa').query_db(query)
        # Create an empty list to append our instances
        likes = []
        # Iterate over the db results and create instances
        for like in results:
            likes.append( cls(like) )
        return likes
    
    @classmethod
    def get_posts_likes(cls, data):
        query = "SELECT * from likes left join posts on posts.pid = likes.post_id where post_id = %(post_id)s;"
        results = connectToMySQL('paa').query_db(query, data)
        # Create an empty list to append our instances
        likes = []
        # Iterate over the db results and create instances
        for like in results:
            likes.append( cls(like) )
        return likes
    
    
    @classmethod
    def get_post_user_like(cls, data):
        query = "SELECT * from likes where post_id = %(post_id)s and user_id = %(user_id)s;"
        results = connectToMySQL('paa').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    
    
    @classmethod
    def add_like(cls, data):
        query = "INSERT INTO likes (user_id, post_id, created_at, updated_at) VALUES (%(user_id)s, %(post_id)s , NOW(), NOW());" # this returns an id
        return connectToMySQL('paa').query_db(query, data)
    
    
    
    @classmethod
    def delete_like(cls, data):
        query = "DELETE from likes where user_id = %(user_id)s and post_id = %(post_id)s;"
        return connectToMySQL('paa').query_db(query, data)
    
    @classmethod
    def delete_post_likes(cls, data):
        query = "DELETE from likes where post_id = %(post_id)s and user_id = %(user_id)s;"
        return connectToMySQL('paa').query_db(query, data)