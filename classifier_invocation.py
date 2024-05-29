import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import io
import os
from flask import Flask, request, jsonify, make_response
import json
from flask_cors import CORS

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

def preprocess_image(image):
    img = Image.open(io.BytesIO(image)).convert('RGB').resize((200, 200))
    img = np.array(img)

    img = img.reshape(1, 200, 200, 3) / 255.0  # 預處理圖片

    # 打印預處理後的圖像數據
    print('Preprocessed image shape:', img.shape)
    print('Preprocessed image data:', img)
    
    return img

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "http://localhost:8000"}})  # 允許從http://localhost:8000請求
                                                                          #cd C:\Users\user\Desktop\專題\畢業專題\分類模型
                                                                          #python -m http.server 8000
#CORS(app)  # 允許所有來源                                                                

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    try:
        image = request.files['image'].read()
        img = preprocess_image(image)

        # 在這裡檢查接收到的圖像數據
        with open('received_image.png', 'wb') as f:
            f.write(image)
        
        img = preprocess_image(image)
        
        # 進行預測
        prediction = model.predict(img)
        predicted_class = label_classes[np.argmax(prediction)]
        
        # 使用 json.dumps 並設置 ensure_ascii=False 回傳中文
        response = make_response(json.dumps({'Predicted Character': predicted_class}, ensure_ascii=False))
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
