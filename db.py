from pymongo import MongoClient,DESCENDING
from werkzeug.security import generate_password_hash
from user import User
import datetime

client = MongoClient('mongodb+srv://pythonchampion187:pythonchampion187@pythonchamp.un2r6q3.mongodb.net/')

chat_db = client.get_database('flask_chat')
users_collection = chat_db.get_collection('users')
rooms_collection = chat_db.get_collection('rooms')
message_collection = chat_db.get_collection('messages')
message_limit = 5

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

def save_room_message(room_id,user_name,message):
    message_collection.insert_one({
        'room_id' : room_id,
        'user_name' : user_name,
        'message' : message,
        'created_on' : datetime.datetime.now()
    })

def get_room_messages(room_name,limit=5,page=1):
    offset = (page - 1) * limit
    messages = list(message_collection.find(
        {'room_id' : room_name}
        ,{'_id' : 0,'room_id' : 0}
        ).skip(offset).limit(limit).sort("created_on", DESCENDING)
        )
    if page == 1:
        messages.reverse()
    return messages

def get_number_of_messages(room_name):
    page = len(list(message_collection.find(
        {'room_id' : room_name}
        ,{'_id' : 0,'room_id' : 0}
        ))) // message_limit
    return page

def delete_message_history(room_name):
    message_collection.delete_many({
        'room_id' : room_name
    })
    return True