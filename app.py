from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
import hashlib
from sqlalchemy.orm import joinedload

app = Flask(__name__)

# 配置数据库 URI
app.secret_key = 'your_secret_key'  # 閃存功能密要
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
    is_filed = db.Column(db.Boolean, default=False)

class UserCredential(db.Model):
    __tablename__ = 'user_credential'
    hash_id = db.Column(db.Integer, primary_key=True)
    hash_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    hash_user_pwd = db.Column(db.String(255), nullable=False)

#取的user憑證
def get_user_with_credentials(account):
    return db.session.query(User, UserCredential).\
        join(UserCredential, User.user_id == UserCredential.hash_user_id).\
        filter(User.account == account).\
        first()


def hash_password(password, salt):
    conbined_String = (password + salt).strip()
    return hashlib.sha256(conbined_String.encode()).hexdigest()

# 根路由
@app.route('/')
def home():
    return render_template('home.html')

# 登錄頁面路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #print(request.form)  # 打印表单数据
        account = request.form.get('account')
        password = request.form.get('password')

        if not account or not password:
            return jsonify({'error': 'Missing account or password'}), 400
        
        user = get_user_with_credentials(account)
        

        if user and user[1].hash_user_pwd.strip() == hash_password(password, user[0].user_salt):
            return redirect(url_for('dashboard'))
        else:
            flash('Ivalid UserID or Password', 'error')
            return redirect(url_for('login'))
        
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
    try:
        # 测试数据库连接
        with app.app_context():
            db.session.execute(text('SELECT 1'))
        print("Database connected successfully")
    except Exception as e:
        print(f"Database connection failed: {e}")
    app.run(debug=True)