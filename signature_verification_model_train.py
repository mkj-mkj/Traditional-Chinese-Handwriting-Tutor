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
        processed_image = preprocess_image(image_path)
        features.append(extract_features(processed_image))
    return np.array(features), np.array(labels)

# 訓練PNN模型並使用網格搜尋調整參數
def train_pnn(features, labels):
    # 將資料分為訓練集 (80%)和測試集 (20%)
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, stratify=labels)

    # 構建管道
    pnn = make_pipeline(StandardScaler(), MLPClassifier(max_iter=500))

    # 定義參數網格
    param_grid = {
        'mlpclassifier__hidden_layer_sizes': [(50,), (100,), (150,)],
        'mlpclassifier__alpha': [0.0001, 0.001, 0.01],
        'mlpclassifier__learning_rate_init': [0.001, 0.01, 0.1]
    }

    # 使用網格搜尋進行參數調整
    min_samples_per_class = min(np.bincount(labels))
    cv_splits = min(5, min_samples_per_class)
    grid_search = GridSearchCV(pnn, param_grid, cv=cv_splits)
    grid_search.fit(X_train, y_train)

    # 獲取最佳參數
    best_params = grid_search.best_params_
    print(f"Best parameters found: {best_params}")

    # 使用最佳參數重新訓練模型
    best_pnn = grid_search.best_estimator_

    # 測試模型
    test_predictions = best_pnn.predict(X_test)
    test_accuracy = accuracy_score(y_test, test_predictions)
    print(f"Test accuracy: {test_accuracy}")

    # 保存模型
    joblib.dump(best_pnn, 'signature_verification.pkl')
    print("Model saved as signature_verification.pkl")

    return best_pnn

# 測試PNN模型
def test_pnn(pnn, test_image_path):
    test_image = preprocess_image(test_image_path)
    test_features = extract_features(test_image).reshape(1, -1)
    prediction = pnn.predict(test_features)
    return prediction

#初次訓練模型(簽名檔路徑、user_id)，兩個輸入都要是陣列(size要一樣大) 例如：update_model(['test_signature.jpg'], [6])、update_model(['test_1.jpg', 'test_2.jpg'], [6, 5])
def signature_verification_train(img_path, label):
    # 準備資料集
    features, labels = prepare_dataset(img_path, label)
    # 訓練PNN模型並調整參數
    train_pnn(features, labels)



'''
# 讀取CSV文件
data = pd.read_csv("./signature_data.csv")

# 打亂資料
data = data.sample(frac=1).reset_index(drop=True)

# print(np.size(image_paths))
# print(np.size(labels))
print(np.bincount(data['name']))

# 準備資料集
features, labels = prepare_dataset(data['img_path'], data['name'])
# 訓練PNN模型並調整參數
pnn = train_pnn(features, labels)

# 測試PNN模型
test_image_path = "test_signature.jpg"  # \測試影像的路徑
prediction = test_pnn(pnn, test_image_path)
print(f"Predicted label: {prediction[0]}")
'''
