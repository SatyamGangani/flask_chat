from flask import Flask,render_template,request,session,redirect,url_for
from flask_socketio import SocketIO,send,join_room,leave_room
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
import os
from db import get_user,save_user,create_room,get_room
from pymongo import errors

app = Flask(__name__)
port = int(os.environ.get("PORT", 8000))
app.secret_key = "SGSGSG"
socketio = SocketIO(app,cors_allowed_origins="*")
login_manager = LoginManager()
# Make login manager know where the login routing is there.
login_manager.login_view = 'login'
login_manager.init_app(app)


@socketio.on("message")
def handle_message():
    pass

@app.route('/chat',methods=['POST','GET'])
@login_required
def handle_chat():
    room_name = request.form.get('room_name')
    # user_name = request.form.get('user_name')
    room_name_pass = request.form.get('room_name_pass')
    room_action = request.form.get('room_action')
    err_message = ''
    if room_action == 'Create':
        try:
            create_room(room_name,room_name_pass)
        except errors.DuplicateKeyError as ex:
            err_message = "Room already exists."
            return render_template('index.html',err_message = err_message,room=room_name)
        return render_template('chat.html',room=room_name,user=current_user.username)
    else:
        room = get_room(room_name)
        if room:
            if room.get('password') == room_name_pass:
                return render_template('chat.html',room=room_name,user=current_user.username)
            else:
                err_message = "Entered room password is wrong."
        else:
            err_message = "Entered room doesn't exist."

        return render_template('index.html',err_message = err_message,room=room_name)

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info(f'{data["username"]} has joined the room : {data["room"]}')
    join_room(room=data['room'])
    socketio.emit('join_room_announcement',data,room=data['room'])

@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info(f'{data["username"]} has message in the room : {data["room"]}')
    socketio.emit('receive_message',data,room=data['room'])

@socketio.on('disconnect')
def on_discount():
    socketio.emit('left_room',data={'username' : current_user.username,'room':session['room']},room=session['room'])   

@login_manager.user_loader
def load_user(username):
    return get_user(username)

@app.route('/login',methods=['POST','GET'])
def login():
    err_message = ""
    user = ''
    # If the user is already logged in then redirecting it home.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('user_name')
        password = request.form.get('password')
        user = get_user(username=username)
        if user and user.is_password_valid(password):
            login_user(user)
            return redirect(url_for('index'))
        if user:
            err_message = "Invalid Password!"
            user = username
        else:
            err_message = "Invalid Username!"

    return render_template('login.html',err_message=err_message,user = user)

@app.route('/signup',methods=['POST','GET'])
def signup():
    err_message = ""
    user = ''
    email = ''
    # If the user is already logged in then redirecting it home.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('user_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user = get_user(username=username)
        
        if user:
            err_message = "Username already exists."
            email = email
            user = username
        elif password != confirm_password:
            err_message = "Password must be same."
            email = email
        else:
            save_user(username,email,password)
            return redirect(url_for('login'))

    return render_template('signup.html',err_message=err_message,user = user,email=email)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app,debug=True,host='127.0.0.0',port=port)