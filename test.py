from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib

app = Flask(__name__)

# 配置数据库 URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义 User 模型
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(45), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_salt = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_filed = db.Column(db.Boolean, default=False)

def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

# 根路由
@app.route('/')
def home():
    return render_template('home.html')

# 登錄頁面路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(account=email).first()
        if user and user.password == hash_password(password, user.user_salt):
            return redirect(url_for('dashboard'))
        else:
            return jsonify({'error': 'Invalid credentials'}), 400
    return render_template('login.html')

# 註冊頁面路由
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(account=email).first():
            return jsonify({'error': 'Email already registered'}), 400

        user_salt = os.urandom(16).hex()
        password_hash = hash_password(password, user_salt)
        new_user = User(name=name, account=email, user_salt=user_salt, password=password_hash)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('sign_up.html')

# 簽名驗證頁面路由
@app.route('/sign_pad')
def sign_pad():
    return render_template('sign_pad.html')

# 儀表板頁面路由
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
