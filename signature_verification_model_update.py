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

# 資料庫準備
def prepare_dataset(image_paths, labels):
    features = []
    for image_path in image_paths:
        #print(image_path)
        processed_image = preprocess_image(image_path)
        features.append(extract_features(processed_image))
    return np.array(features), np.array(labels)

# 增量更新函數
def add_samples_to_model(pnn, X_new, y_new, classes, best_params):
    # 使用最佳參數初始化模型
    mlp = MLPClassifier(max_iter=500,
                        hidden_layer_sizes=best_params['mlpclassifier__hidden_layer_sizes'],
                        alpha=best_params['mlpclassifier__alpha'],
                        learning_rate_init=best_params['mlpclassifier__learning_rate_init'])
    scaler = StandardScaler()

    # 拆分pnn管道
    for step in pnn.steps:
        if isinstance(step[1], StandardScaler):
            scaler = step[1]
        if isinstance(step[1], MLPClassifier):
            mlp = step[1]

    # 使用新的資料進行部分擬和
    X_new_scaled = scaler.transform(X_new)
    mlp.partial_fit(X_new_scaled, y_new, classes=classes)

    # 重新构建管道
    new_pnn = make_pipeline(scaler, mlp)
    joblib.dump(new_pnn, 'signature_verification.pkl')
    print("Model updated and saved as signature_verification.pkl")

# 更新模型(新增的簽名檔路徑、user_id)，兩個輸入都要是陣列(size要一樣大) 例如：update_model(['test_signature.jpg'], [6])、update_model(['test_1.jpg', 'test_2.jpg'], [6, 5])
def update_model(img_path, label):
    pnn = joblib.load('signature_verification.pkl')
    features, labels = prepare_dataset(img_path, label)
    add_samples_to_model(pnn, features, labels, classes=pnn.classes_, best_params=pnn.get_params())

#update_model(['test_signature.jpg'], [6])