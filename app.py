# app.py
from flask import Flask, request, jsonify
import hashlib,sqlite3
import os
from dbsetup import Database
from observer import notifier, Emailnotifier
from strategy import Validate, emailvalidation, passwordvalidation

app = Flask(__name__)

notifier = notifier()
notifier.attach(Emailnotifier())


email_validator = Validate(emailvalidation())
password_validator = Validate(passwordvalidation())


@app.route("/registration", methods=["POST"])
def registration():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"Status": "Error", "message": "username, email, and password are required"}), 400

    if not email_validator.is_valid(email):
        return jsonify({"Status": "Error", "message": "Invalid email"}), 400
    if not password_validator.is_valid(password):
        return jsonify({"Status": "Error", "message": "Weak password (min 8 chars & include digit)"}), 400

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    
    db = Database()
    try:
        db.cursor.execute(
            "INSERT INTO user (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password) )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"Status": "Error", "message": "Username or email already exists"}), 400

   
    user_data = {"username": username, "email": email}
    notifier.notify("Registration", user_data)

    return jsonify({"Status": "Success", "message": "User registered successfully"}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"Status": "Error", "message": "Email and password are required"}), 400

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    db = Database()
    db.cursor.execute("SELECT username, password FROM user WHERE email=?", (email,))
    row = db.cursor.fetchone()

    if not row:
        return jsonify({"Status": "Error", "message": "User not found"}), 404

    username, saved_password = row
    if saved_password != hashed_password:
        return jsonify({"Status": "Error", "message": "Incorrect password"}), 401

    return jsonify({"Status": "Success", "message": f"Welcome back, {username}!"}), 200


if __name__ == "__main__":
    app.run(debug=True)


