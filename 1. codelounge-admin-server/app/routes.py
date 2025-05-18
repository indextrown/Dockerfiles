from app import app
import pyrebase
from flask import render_template, request, jsonify, redirect, url_for, session
from functools import wraps
import os
from dotenv import load_dotenv

# Firebase 설정
config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DB_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE"),
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
app.secret_key = 'your_secret_key'  # 세션 암호화 키

# 인증 데코레이터
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 관리자 권한 데코레이터
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return jsonify({'error': 'Admin only'}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin = db.child("Admins").child(username).get().val()
        if admin and admin.get("password") == password:
            session["user"] = username
            session["is_admin"] = True
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def home():
    # Firebase 데이터 가져오기
    data = db.child("Posts").get().val() or {}  # Posts 아래의 모든 카테고리 데이터 가져오기
    return render_template("index.html", data=data, is_admin=session.get('is_admin'))

@app.route("/add-entry", methods=["POST"])
@login_required
@admin_required
def add_entry():
    data = request.json
    category = data.get("category")
    title = data.get("title")
    author = data.get("author")
    time = data.get("time")
    content = data.get("content")

    if not all([category, title, author, time, content]):
        return jsonify({"error": "All fields are required"}), 400

    try:
        # Posts 아래의 카테고리에서 모든 키 가져오기
        existing_keys = db.child("Posts").child(category).get().val() or {}
        
        # 가장 큰 "No-{number}" 찾기
        max_number = 0
        for key in existing_keys.keys():
            if key.startswith("No-") and key[3:].isdigit():
                max_number = max(max_number, int(key[3:]))

        # 새 번호 생성
        new_number = max_number + 1 if max_number > 0 else 1
        new_key = f"No-{new_number}"

        # 새로운 데이터 추가
        new_entry = {
            "title": title,
            "author_id": author,
            "created_at": time,
            "content": content,
        }
        db.child("Posts").child(category).child(new_key).set(new_entry)

        return jsonify({"success": True, "new_key": new_key}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route("/update-entry", methods=["POST"])
@login_required
@admin_required
def update_entry():
    data = request.json
    category = data.get("category")
    title = data.get("title")
    author = data.get("author")
    time = data.get("time")
    content = data.get("content")
    key = data.get("key")

    if not all([category, title, author, time, content, key]):
        return jsonify({"error": "All fields and a valid key are required"}), 400

    try:
        updated_entry = {
            "title": title,
            "author_id": author,
            "created_at": time,
            "content": content,
        }
        db.child("Posts").child(category).child(key).update(updated_entry)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete-entry", methods=["POST"])
@login_required
@admin_required
def delete_entry():
    data = request.json
    category = data.get("category")
    key = data.get("key")

    if not category or not key:
        return jsonify({"error": "Category and key are required"}), 400

    try:
        db.child("Posts").child(category).child(key).remove()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
