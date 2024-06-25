from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from user import User

client = MongoClient('mongodb+srv://pythonchampion187:pythonchampion187@pythonchamp.un2r6q3.mongodb.net/')

chat_db = client.get_database('flask_chat')
users_collection = chat_db.get_collection('users')
rooms_collection = chat_db.get_collection('rooms')

def save_user(username,email,password):
    hash_password = generate_password_hash(password)
    users_collection.insert_one({
        '_id' : username,
        'email' : email,
        'password' : hash_password
    })

def get_user(username):
    user_data = users_collection.find_one({'_id':username})
    if user_data:
        return User(user_data['_id'],user_data['email'],user_data['password'])
    return None

def get_room(room_name):
    room_data = rooms_collection.find_one({'_id':room_name})
    if room_data:
        return room_data
    return None

def create_room(room_name,room_passwword):
    rooms_collection.insert_one({
        '_id' : room_name,
        'password' : room_passwword
    })
    return True