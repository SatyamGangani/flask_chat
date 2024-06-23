from flask import Flask,render_template,request
from flask_socketio import SocketIO,send,join_room

app = Flask(__name__)


socketio = SocketIO(app,cors_allowed_origins="*")

@socketio.on("message")
def handle_message():
    pass

@app.route('/chat',methods=['POST','GET'])
def handle_chat():
    room_name = request.form.get('room_name')
    user_name = request.form.get('user_name')
    return render_template('chat.html',room=room_name,user=user_name)

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info(f'{data["username"]} has joined the room : {data["room"]}')
    join_room(room=data['room'])
    socketio.emit('join_room_announcement',data)

@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info(f'{data["username"]} has message in the room : {data["room"]}')
    socketio.emit('receive_message',data,room=data['room'])

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app,debug=True)