from flask import request
from flask_socketio import emit
from .extensions import socketio

# Create an empty dictionary
users = {}

# --------------------
# Show when connected
@socketio.on("connect")
def handle_connect():
    print("Client connected!")

# ----------------------
# Display a username
@socketio.on("user_join")
def handle_user(username):
    print(f"User {username} has joined")

# ----------------------
# Display a message
@socketio.on("new_message")
def handle_message(message):
    print(f"Message: {message}")
    username = None
    
    for user in users:
        if users[user] == request.sid:
            username = user
    emit("chat", {"message": message, "username": username}, broadcast=True)