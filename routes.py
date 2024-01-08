from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/chatroom")
def chatroom():
    return render_template("chatroom.html")
