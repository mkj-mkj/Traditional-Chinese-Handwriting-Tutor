from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import base64

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

class HandwritingUpload(db.Model):
    __tablename__ = 'handwriting_upload'
    upload_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    image_data = db.Column(db.Text, nullable=False)  # 存儲圖片的Base64編碼
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('uploads', lazy=True))

# 創建資料庫和遷移
with app.app_context():
    db.create_all()

# 提交手寫資料
@app.route('/upload_handwriting', methods=['POST'])
def upload_handwriting():
    file = request.files['image']
    user_id = request.form.get('user_id', type=int, default=1)  # 假設用戶ID為1，實際應從用戶登錄信息中獲取
    image_data = base64.b64encode(file.read()).decode('utf-8')

    new_upload = HandwritingUpload(
        user_id=user_id,
        image_data=image_data
    )
    db.session.add(new_upload)
    db.session.commit()
    return jsonify({'message': 'Handwriting data uploaded successfully'}), 201

# 獲取用戶的手寫上傳資料
@app.route('/handwriting/<int:user_id>', methods=['GET'])
def get_handwriting(user_id):
    uploads = HandwritingUpload.query.filter_by(user_id=user_id).all()
    if uploads:
        return jsonify([{
            'upload_id': upload.upload_id,
            'user_id': upload.user_id,
            'image_data': upload.image_data,
            'timestamp': upload.timestamp.isoformat()
        } for upload in uploads]), 200
    else:
        return jsonify({'error': 'No uploads found for this user'}), 404

if __name__ == '__main__':
    app.run(debug=True)
