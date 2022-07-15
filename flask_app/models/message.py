from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 


class Message:
    def __init__(self, data):
        self.mid = data['mid']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.sender = data['sender']
        self.receiver = data['receiver']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']        
        
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM messages;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('paa').query_db(query)
        # Create an empty list to append our instances
        messages = []
        # Iterate over the db results and create instances
        for message in results:
            messages.append( cls(message) )
        return messages
    
    
    
    
    @classmethod
    def get_user_messages(cls, data):
        query = "SELECT users.first_name as sender, users2.first_name as receiver, messages.* from users LEFT JOIN messages on users.id = messages.sender_id LEFT JOIN users as users2 on users2.id = messages.receiver_id where ( sender_id = %(sender_id)s and receiver_id = %(receiver_id)s ) or (sender_id = %(receiver_id)s and receiver_id = %(sender_id)s );"
        # this query gets all the messages between two users. User in session will always be sender and other user will always be the receiver. 
        # So we are getting all messages where 
        # sender and receiver will be the person in session OR the sender and receiver will be the other user
        results = connectToMySQL('paa').query_db(query, data)
        messages = []
        for message in results:
            messages.append(cls(message))
        return messages
    
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO messages ( content , sender_id, receiver_id, created_at, updated_at ) VALUES ( %(content)s , %(sender_id)s, %(receiver_id)s, NOW() , NOW() );" # will return id can also be called create
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('paa').query_db( query, data ) 
    
    @classmethod
    def get_message(cls, data):
        query = "SELECT * from messages where mid = %(mid)s;"
        results = connectToMySQL('paa').query_db(query, data)
        return cls(results[0])
    
    
    @classmethod
    def update_message(cls, data):
        query = "UPDATE messages SET content = %(content)s, created_at = NOW(), updated_at = NOW() WHERE mid = %(mid)s;"
        return connectToMySQL('paa').query_db(query, data)
    
    
    @classmethod
    def delete(cls, data):
        query = "DELETE from messages where mid = %(mid)s;"
        return connectToMySQL('paa').query_db(query, data)