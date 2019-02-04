import os
from flask import Flask, redirect, render_template, request, session, url_for
from datetime import datetime

app= Flask(__name__)
messages = []
app.secret_key = "randomstring123"

def add_message(username, message):
    """Takes our username and message and appends it to the list"""
    now = datetime.now().strftime("%H:%M:%S")
    messages.append({"timestamp" :now, "from":username, "message":message})

@app.route("/", methods=["GET", "POST"])
def index():
    """Main page with instructions"""
    if request.method == "POST":
        session["username"] = request.form["username"]

    if "username" in session:
        return redirect(url_for("user", username=session["username"]))

    return render_template("index.html")
    
@app.route('/chat/<username>', methods = ["GET", "POST"])
def user(username):
    """Add and display chat message"""
    if request.method == "POST":
        username = session["username"]
        message = request.form["message"]
        add_message(username, message)
        return redirect(url_for("user", username=session["username"]))

    return render_template("chat.html", username=username, chat_messages=messages)
    
    
app.run(host= os.getenv('IP'), port= int(os.getenv('PORT')), debug= True)
