from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
import os
import binascii
import hashlib
from functools import wraps

app = Flask(__name__)

# 使用 SQLite 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 設置郵件服務
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# 定義模型
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(45), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_salt = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    external_account = db.Column(db.String(100), nullable=True)

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(45), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    admin_salt = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    is_superadmin = db.Column(db.Boolean, default=False)  # 標示是否是高階管理者

# 創建資料庫和遷移
with app.app_context():
    db.create_all()

# 檢查高階管理者權限
def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.current_admin.is_superadmin:
            return jsonify({'error': 'Superadmin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# 從請求中提取當前管理者信息
@app.before_request
def get_current_admin():
    admin_id = request.headers.get('Admin-ID')
    if admin_id:
        g.current_admin = Admin.query.get(admin_id)

# 增加管理者
@app.route('/admins', methods=['POST'])
@superadmin_required
def add_admin():
    data = request.get_json()
    admin_salt = binascii.hexlify(os.urandom(16)).decode('utf-8')
    password_hash = hash_password(data['password'], admin_salt)
    new_admin = Admin(
        account=data['account'],
        name=data['name'],
        admin_salt=admin_salt,
        password=password_hash,
        email=data['email'],
        is_superadmin=data.get('is_superadmin', False)
    )
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({'message': 'Admin added successfully'}), 201

# 查看管理者
@app.route('/admins/<int:admin_id>', methods=['GET'])
@superadmin_required
def get_admin(admin_id):
    admin = Admin.query.get(admin_id)
    if admin:
        return jsonify({
            'admin_id': admin.admin_id,
            'account': admin.account,
            'name': admin.name,
            'email': admin.email,
            'is_superadmin': admin.is_superadmin
        }), 200
    else:
        return jsonify({'error': 'Admin not found'}), 404

# 修改管理者
@app.route('/admins/<int:admin_id>', methods=['PUT'])
@superadmin_required
def update_admin(admin_id):
    data = request.get_json()
    admin = Admin.query.get(admin_id)
    if admin:
        admin.account = data.get('account', admin.account)
        admin.name = data.get('name', admin.name)
        admin.email = data.get('email', admin.email)
        admin.is_superadmin = data.get('is_superadmin', admin.is_superadmin)
        if 'password' in data:
            admin_salt = binascii.hexlify(os.urandom(16)).decode('utf-8')
            admin.password = hash_password(data['password'], admin_salt)
            admin.admin_salt = admin_salt
        db.session.commit()
        return jsonify({'message': 'Admin updated successfully'}), 200
    else:
        return jsonify({'error': 'Admin not found'}), 404

# 刪除管理者
@app.route('/admins/<int:admin_id>', methods=['DELETE'])
@superadmin_required
def delete_admin(admin_id):
    admin = Admin.query.get(admin_id)
    if admin:
        db.session.delete(admin)
        db.session.commit()
        return jsonify({'message': 'Admin deleted successfully'}), 200
    else:
        return jsonify({'error': 'Admin not found'}), 404

# Hash
def hash_password(password, salt):
    pbkdf2_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000, dklen=32)
    return binascii.hexlify(pbkdf2_hash).decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True)
