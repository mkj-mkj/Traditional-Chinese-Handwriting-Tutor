import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import cv2
import io
import os
from flask import Blueprint, request, jsonify, make_response, session
import json
from flask_cors import CORS
import pickle
import joblib
from signature_verification_prediction import signature_verification


signature_verification_bp = Blueprint('signature_verification', __name__)


#把numpy class轉換成 Json serializable object
class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating, np.bool_)):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(JsonEncoder, self).default(obj)

# 使用正確的檔案路徑
#model_path = r'.\signature_verification.pkl' # 替換路徑
model_path = r'C:\xampp\htdocs\signature_verification\signature_verification.pkl'

# 確認檔案是否存在
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

#app = Flask(__name__)
#CORS(app)
#CORS(app, resources={r"/predict": {"origins": "http://localhost:8000"}})  # 允許從http://localhost:8000請求
                                                                          #cd C:\Users\user\Desktop\專題\畢業專題\分類模型
                                                                          #python -m http.server 8000
                                                               
# API路由
@signature_verification_bp.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    try:
        image = request.files['image'].read()
        prediction = signature_verification(image)
        predicted_class = int(prediction)

        user_id = session.get('user_id')  # 從session中取user_id
        print(f"predicted_class: {predicted_class}, type: {type(predicted_class)}")
        print(f"user_id: {user_id}, type: {type(user_id)}")

        if user_id is None:
            return jsonify({'error': 'User not logged in'}), 401
        
        if predicted_class == int(user_id):
            verification_result = '符合'
        else:
            verification_result = '不符合'

        response = make_response(json.dumps({'Verification Result': verification_result}, ensure_ascii=False))
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500
