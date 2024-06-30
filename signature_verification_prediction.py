import cv2
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score
import joblib

# 影像前處理函數
def preprocess_image(image_path):
    # 讀取影像
    image = cv2.imread(image_path)
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

# 統計式特徵分析
def statistical_feature_analysis(image):
    mean = np.mean(image)
    std_dev = np.std(image)
    return np.array([mean, std_dev])

# 投影量分析
def projection_feature_analysis(image):
    horizontal_projection = np.sum(image, axis=1)
    vertical_projection = np.sum(image, axis=0)
    return np.concatenate((horizontal_projection, vertical_projection))

# 交叉點分析
def crossing_points_analysis(image):
    crossing_points = 0
    for row in image:
        row_crossings = np.sum((row[:-1] == 0) & (row[1:] == 255)) + np.sum((row[:-1] == 255) & (row[1:] == 0))
        crossing_points += row_crossings
    for col in image.T:
        col_crossings = np.sum((col[:-1] == 0) & (col[1:] == 255)) + np.sum((col[:-1] == 255) & (col[1:] == 0))
        crossing_points += col_crossings
    return np.array([crossing_points])

# 特徵提取函數
def extract_features(image):
    stats_features = statistical_feature_analysis(image)
    proj_features = projection_feature_analysis(image)
    crossing_features = crossing_points_analysis(image)
    return np.concatenate((stats_features, proj_features, crossing_features))

# Pnn模型預測
def predict_pnn(pnn, test_image_path):
    test_image = preprocess_image(test_image_path)
    test_features = extract_features(test_image).reshape(1, -1)
    prediction = pnn.predict(test_features)
    return prediction

# 簽名驗證 輸入為簽名檔路徑(單一檔案)，回傳預測類別
def signature_verification(img_path):
    pnn = joblib.load('signature_verification.pkl')
    prediction = predict_pnn(pnn, img_path)
    print(f"Predicted label: {prediction[0]}")
    return prediction[0]

'''
# 測試PNN模型
test_image_path = "test_signature.jpg"  # \測試影像的路徑
prediction = test_pnn(pnn, test_image_path)
print(f"Predicted label: {prediction[0]}")
'''
