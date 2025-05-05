import json
from flask import Flask, render_template, request, flash, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'
USER_DATA_FILE = 'users.json'

def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

users = load_users()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username not in users:
            flash("账号不存在，请先注册。")
        elif users[username] != password:
            flash("密码错误，请重新输入。")
        else:
            return f"登录成功！欢迎你，{username}！"

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if username in users:
            flash("用户名已存在，请更换用户名。")
        elif password != confirm_password:
            flash("两次输入的密码不一致，请重新输入。")
        else:
            users[username] = password
            save_users(users)
            flash("注册成功，请登录。")
            return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)