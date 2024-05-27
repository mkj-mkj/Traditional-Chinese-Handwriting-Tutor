import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import os

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
def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB').resize((200, 200))  
    img = np.array(img).reshape(1, 200, 200, 3) / 255.0  # 預處理圖片
    return img

# 讀取圖片
image_path = r'C:\Users\user\Desktop\專題\畢業專題\分類模型\example.png'  # 替換圖片路徑

# 確認圖片檔案是否存在
if not os.path.exists(image_path):
    raise FileNotFoundError(f"Image file not found: {image_path}")

img = preprocess_image(image_path)

# 進行預測
prediction = model.predict(img)
predicted_class = label_classes[np.argmax(prediction)]

# 輸出預測結果
print('Predicted Character:', predicted_class)
