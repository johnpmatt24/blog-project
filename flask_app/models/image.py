from flask_app.config.mysqlconnection import connectToMySQL

class Image:
    def __init__(self, data):
        self.id = data["id"]
        self.file = data["file"]
        self.user_id = data["user_id"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        
    
    @classmethod
    def get_all(cls):
        query = "SELECT * from images;"
        results = connectToMySQL('paa').query_db(query)
        # Create an empty list to append our instances
        images = []
        # Iterate over the db results and create instances
        for image in results:
            images.append( cls(image) )
        return images
    
    @classmethod
    def get_user_image(cls, data):
        query = "SELECT * from images left join users on users.id = images.user_id where user_id = %(user_id)s;"
        results = connectToMySQL('paa').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    
    
    @classmethod
    def add_image(cls, data):
        query = "INSERT INTO images ( file, user_id, created_at, updated_at) VALUES (%(file)s, %(user_id)s,  NOW(), NOW());" # this returns an id
        return connectToMySQL('paa').query_db(query, data)
    
    
    
    @classmethod
    def update_image(cls, data):
        query = "UPDATE images SET file = %(file)s, created_at = NOW(), updated_at = NOW() WHERE user_id = %(user_id)s;"
        return connectToMySQL('paa').query_db(query, data)
    
    
    @classmethod
    def delete_image(cls, data):
        query = "DELETE from images where user_id = %(user_id)s;"
        return connectToMySQL('paa').query_db(query, data)