from flask import Flask, request, jsonify, make_response
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import io
import os
import json


# 使用正確的檔案路徑
model_path = r'C:\Users\user\Desktop\專題\畢業專題\分類模型\cnn_hanzi_classifier.h5'  # 替換路徑
labels_path = r'C:\Users\user\Desktop\專題\畢業專題\分類模型\label_classes.npy'  # 替換路徑

# 確認檔案是否存在
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

if not os.path.exists(labels_path):
    raise FileNotFoundError(f"Labels file not found: {labels_path}")

# 載入模型和標籤
model = load_model(model_path)
label_classes = np.load(labels_path, allow_pickle=True)

# 定義預處理函數
def preprocess_image(image):
    img = Image.open(io.BytesIO(image)).convert('RGB').resize((200, 200))
    img = np.array(img).reshape(1, 200, 200, 3) / 255.0  # 預處理圖片
    return img

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_api(img):
    if img is None:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image = request.files['image'].read()
        img = preprocess_image(image)

    prediction = model.predict(img)
    predicted_class = label_classes[np.argmax(prediction)]
    
    # 使用 json.dumps 並設置 ensure_ascii=False 回傳中文
    response = make_response(json.dumps({'Predicted Character': predicted_class}, ensure_ascii=False))
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(debug=True)
