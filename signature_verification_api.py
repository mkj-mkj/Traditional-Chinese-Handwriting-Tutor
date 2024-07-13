import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import cv2
import io
import os
from flask import Flask, request, jsonify, make_response
import json
from flask_cors import CORS
import pickle

# 使用正確的檔案路徑
model_path = r'C:\xampp\htdocs\signature_verification\signature_verification.pkl' # 替換路徑

# 確認檔案是否存在
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

# 載入模型和標籤
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# 定義預處理函數
def preprocess_image(image_bytes):
    # 將二進位資料轉換為NumPy陣列
    image_array = np.frombuffer(image_bytes, np.uint8)
    # 解碼影像
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    
    # 灰階轉換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 二值化
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    # 膨脹
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=1)
    # 調整大小
    resized = cv2.resize(dilated, (256, 256))
    
    return resized


app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/predict": {"origins": "http://localhost:8000"}})  # 允許從http://localhost:8000請求
                                                                          #cd C:\Users\user\Desktop\專題\畢業專題\分類模型
                                                                          #python -m http.server 8000
                                                                

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    try:
        image = request.files['image'].read()
        img = preprocess_image(image)
        
        # 進行預測
        prediction = model.predict(img)
        #predicted_class = label_classes[np.argmax(prediction)]
        
        # 使用 json.dumps 並設置 ensure_ascii=False 回傳中文
        response = make_response(json.dumps({'Predicted Character': predicted_class}, ensure_ascii=False))
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        app.logger.error('An error occurred: %s', str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)