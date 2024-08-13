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
import os

#取得模型路徑
def get_model_path():
    current_directory = os.path.dirname(os.getcwd())
    model_path = os.path.join(current_directory, 'signature_verification.pkl')
    return model_path
    
def get_data_path():
    current_directory = os.path.dirname(os.getcwd())
    data_path = os.path.join(current_directory, 'signature_data.npz')
    return data_path

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

def save_data(features, labels):
    data_path = get_data_path()
    data_path = './signature_data.npz'
    if os.path.exists(data_path):
        # 如果已有資料，載入並合併
        data = np.load(data_path)
        X_old = data['features']
        y_old = data['labels']
        # print(X_old)
        # print(y_old)
        X_combined = np.vstack((X_old, features))
        y_combined = np.hstack((y_old, labels))
        # print(X_combined)
        # print(y_combined)
    else:
        # 否則，直接保存
        X_combined = features
        y_combined = labels
    
    np.savez(data_path, features=X_combined, labels=y_combined)

def load_all_data():
    data_path = './signature_data.npz'
    if os.path.exists(data_path):
        data = np.load(data_path)
        return data['features'], data['labels']
    else:
        return None, None

# 增量更新函數
def add_samples_to_model(pnn, X_new, y_new, classes, best_params):

    # 保存新資料
    save_data(X_new, y_new)
    
    # 載入所有資料並訓練
    X_all, y_all = load_all_data()
    print(X_all)
    print(y_all)

    # 確保資料的長度一致
    if X_all.shape[0] != y_all.shape[0]:
        raise ValueError(f"樣本數量不一致：特徵數量 {X_all.shape[0]} 和標籤數量 {y_all.shape[0]} 不一致。")

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
    # print(y_all)
    # print(classes)
    # 使用新的資料進行部分擬和
    X_all_scaled = scaler.transform(X_all)
    mlp.fit(X_all_scaled, y_all)

    # 重新建構管道
    new_pnn = make_pipeline(scaler, mlp)
    model_path = get_model_path()
    joblib.dump(new_pnn, './signature_verification.pkl')
    print(new_pnn.classes_)
    print("Model updated and saved as signature_verification.pkl")

# 更新模型(新增的簽名檔路徑、user_id)，兩個輸入都要是陣列(size要一樣大) 例如：update_model(['test_signature.jpg'], [6])、update_model(['test_1.jpg', 'test_2.jpg'], [6, 5])
def update_model(img_path, label):
    model_path = get_model_path()
    # pnn = joblib.load(model_path)
    pnn = joblib.load('./signature_verification.pkl')
    features, labels = prepare_dataset(img_path, label)
    existing_classes = list(pnn.classes_)
    new_classes = np.unique(np.concatenate((existing_classes, label)))
    add_samples_to_model(pnn, features, labels, classes=new_classes, best_params=pnn.get_params())



# # 讀取CSV文件
# data = pd.read_csv("./signature_data.csv")

# # 打亂資料
# data = data.sample(frac=1).reset_index(drop=True)

# update_model(['test1.jpg','test2.jpg'], [10,10])
