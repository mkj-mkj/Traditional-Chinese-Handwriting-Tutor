import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import io
import os
from flask import Flask, request, jsonify, make_response
import json
from flask_cors import CORS

# 使用正確的檔案路徑
model_path = r'.\cnn_hanzi_classifier.h5'  # 替換路徑
labels_path = r'.\label_classes.npy'  # 替換路徑

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
    img_np = np.array(img)

    # 建立一個白色的圖像，形狀為 (200, 200, 4)
    blank_image = Image.new("RGBA", img.size, (255, 255, 255, 255))
    blank_np = np.array(blank_image)

    # 建立一個黑色遮罩
    black_mask = np.all(img_np[:, :, :3] < 50, axis=-1)

    # 將黑色部分設置為原始圖像的像素
    blank_np[black_mask, :3] = img_np[black_mask]

    # 轉換回圖像
    cleaned_red_image = Image.fromarray(blank_np)
    # cleaned_red_image.save('./test.png')

    # 將預處理結果轉換為 (1, 200, 200, 3) 並歸一化
    cleaned_red_image = blank_np[:, :, :3].reshape(1, 200, 200, 3) / 255.0  # 預處理圖片
    
    return cleaned_red_image

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
        predicted_class = label_classes[np.argmax(prediction)]
        
        # 使用 json.dumps 並設置 ensure_ascii=False 回傳中文
        response = make_response(json.dumps({'Predicted Character': predicted_class}, ensure_ascii=False))
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        app.logger.error('An error occurred: %s', str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)