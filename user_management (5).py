from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import binascii
import hashlib

app = Flask(__name__)

# 使用 SQLite 作為臨時測試的資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 定義模型
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(45), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_salt = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)

# 創建資料庫和遷移
with app.app_context():
    db.create_all()

# 增加用戶
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    user_salt = binascii.hexlify(os.urandom(16)).decode('utf-8')
    password_hash = hash_password(data['password'], user_salt)
    new_user = User(
        account=data['account'],
        name=data['name'],
        user_salt=user_salt,
        password=password_hash
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'}), 201

# 查看用戶
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'user_id': user.user_id,
            'account': user.account,
            'name': user.name,
            'user_salt': user.user_salt,
            'password': user.password
        }), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# 修改用戶
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if user:
        user.account = data.get('account', user.account)
        user.name = data.get('name', user.name)
        if 'password' in data:
            user_salt = binascii.hexlify(os.urandom(16)).decode('utf-8')
            user.password = hash_password(data['password'], user_salt)
            user.user_salt = user_salt
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# 刪除用戶
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# 哈希密碼
def hash_password(password, salt):
    pbkdf2_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000, dklen=32)
    return binascii.hexlify(pbkdf2_hash).decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True)


