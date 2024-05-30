import cv2
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV

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
    # 構建管道
    pnn = make_pipeline(StandardScaler(), MLPClassifier(max_iter=500))

    # 定義參數網格
    param_grid = {
        'mlpclassifier__hidden_layer_sizes': [(50,), (100,), (150,)],
        'mlpclassifier__alpha': [0.0001, 0.001, 0.01],
        'mlpclassifier__learning_rate_init': [0.001, 0.01, 0.1]
    }

    # 使用網格搜尋進行參數調整
    grid_search = GridSearchCV(pnn, param_grid, cv=5)
    grid_search.fit(features, labels)

    # 獲取最佳參數
    best_params = grid_search.best_params_
    print(f"Best parameters found: {best_params}")

    # 使用最佳參數重新訓練模型
    best_pnn = grid_search.best_estimator_
    return best_pnn

# 測試PNN模型
def test_pnn(pnn, test_image_path):
    test_image = preprocess_image(test_image_path)
    test_features = extract_features(test_image).reshape(1, -1)
    prediction = pnn.predict(test_features)
    return prediction

# 主函數
if __name__ == "__main__":
    # 假設資料庫中有20個人的簽名，每人10筆簽名
    image_paths = ["signature_1.png", "signature_2.png", ..., "signature_200.png"]  # 請填入實際影像路徑
    labels = [1, 1, ..., 20]  # 請填入對應的標籤

    # 準備資料集
    features, labels = prepare_dataset(image_paths, labels)

    # 訓練PNN模型並調整參數
    pnn = train_pnn(features, labels)

    # 測試PNN模型
    test_image_path = "test_signature.png"  # 請填入測試影像的路徑
    prediction = test_pnn(pnn, test_image_path)
    print(f"Predicted label: {prediction[0]}")
