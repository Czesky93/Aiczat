
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "full_project_with_menu"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///full_project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

@app.route("/")
def home():
    # Dynamically populate the menu based on available routes and modules
    modules = [
        {"name": "Dashboard", "url": "/dashboard"},
        {"name": "Settings", "url": "/settings"},
        {"name": "AI Interaction", "url": "/ai_interaction"}
    ]
    return render_template("index.html", modules=modules)

@app.route("/dashboard")
def dashboard():
    logs = Log.query.order_by(Log.timestamp.desc()).all()
    return render_template("dashboard.html", logs=logs)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exists!", "warning")
        else:
            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("User registered successfully!", "success")
        return redirect(url_for("settings"))
    return render_template("settings.html")

@app.route("/ai_interaction", methods=["GET", "POST"])
def ai_interaction():
    if request.method == "POST":
        command = request.form.get("command", "").lower()
        if "analyze" in command:
            result = "AI is analyzing the data..."
        elif "update" in command:
            result = "AI is updating the system..."
        else:
            result = "AI did not understand the command."
        return render_template("ai_interaction.html", result=result)
    return render_template("ai_interaction.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
