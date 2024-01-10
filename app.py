## Import necessary libraries
from flask import Flask, render_template, url_for, redirect, session, request
from flask_bootstrap import Bootstrap
from models import LoginForm, User, RegisterForm, db, login_man
from flask_sqlalchemy import SQLAlchemy
# from passlib.hash import pbkdf2_sha256
from flask_login import login_required, login_user
#from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissecret'
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# ------------------
# Inits
Bootstrap(app)
db.init_app(app)
login_man.init_app(app)

# Create empty dictionary to hold rooms usr creates
rooms = {}

# ------------------------------
# Create a unique room code
def generate_unique_code(length):
    """Create a unique code for each room"""
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

@app.route("/home", methods=["POST", "GET"])
# @login_required
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

# ---------------------
# Route for chatroom
@app.route("/room")
def room():
    """Chatroom feature"""
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

# ---------------------
# Socketio logic

@socketio.on("message")
def message(data):
    """Handle messages in the chat"""
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    """Handle auth and connections to chat"""
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    """Handle when a usr is disconnected"""
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")
    
# ------------------
# Route to home page
@app.route('/')
def home_page():
    return render_template('index.html')

# -------------------
# Route for signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    
    if form.validate_on_submit():
        # hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been created!</h1>'
        
    return render_template('signup.html', form=form)

# -------------------
# Route for FAQ page
@app.route('/faq')
def faq():
    return render_template('faq.html')

# ------------------
# Route for Features page
@app.route('/features')
def features():
    return render_template('features.html')

# -------------------
# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user, remember=form.remember_session.data)
                return redirect(url_for('home'))
        return '<h1>Invalid username or password</h1>'
        
    return render_template('login.html', form=form)

if __name__ == "__main__":
    socketio.run(app, debug=False)
    
