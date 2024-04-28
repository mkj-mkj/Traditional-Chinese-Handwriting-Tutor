import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras.utils import to_categorical
import tensroflow.keras.layers as layers

# 假設圖像資料夾路徑和標籤文件路徑
image_folder = 'path_to_images'
train_label_csv = 'path_to_train_labels.csv'
test_label_csv = 'path_to_test_labels.csv'

N = 12  # N是書寫規則數量

# 載入和預處理圖像，包括數據增強
def preprocess_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_png(image, channels=1)
    image = tf.image.resize(image, [200, 200])

    # 數據增強：隨機左右翻轉
    image = tf.image.random_flip_left_right(image)

    # 數據增強：隨機調整亮度
    image = tf.image.random_brightness(image, max_delta=0.3)

    # 數據增強：筆劃加粗，透過膨脹實作
    kernel = tf.ones((3, 3, 1, 1), tf.float32)  # 定義膨脹所使用的核
    image = tf.nn.dilation2d(
        image[tf.newaxis, ..., tf.newaxis],
        filters=kernel,
        strides=[1, 1, 1, 1],
        padding="SAME"
    )[0, ..., 0]
    
    image /= 255.0  # 歸一化到0-1
    return image

# 載入標籤和圖像路徑
def load_data(label_csv, image_folder):
    labels_df = pd.read_csv(label_csv)
    image_paths = labels_df['image'].apply(lambda x: f"{image_folder}/{x}")
    labels = labels_df['label'].values
    images = np.array([preprocess_image(path).numpy() for path in image_paths])
    labels = to_categorical(labels, num_classes=2**N)  
    return images, labels

# 載入訓練和測試數據
train_images, train_labels = load_data(train_label_csv, image_folder)
test_images, test_labels = load_data(test_label_csv, image_folder)

# 定義模型
model = tf.keras.models.Sequential([
    #輸入層和第一層卷積層
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(200, 200, 1)),
    layers.MaxPooling2D((2, 2)),
    #第二層卷積層
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    #第三層卷積層
    layers.Conv2D(128, (3, 3), activation='relu'),
    #第四層卷積層
    layers.Conv2D(256, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    #展平層，將多維輸入一維化
    layers.Flatten(),
    #第一層全連接層
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.5),
    #第二層全連接層
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    #第三層全連接層
    layers.Dense(2**N, activation='softmax')  
])

# 編譯模型
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 訓練模型
history = model.fit(train_images, train_labels, epochs=80, validation_split=0.1)

# 評估模型
test_loss, test_accuracy = model.evaluate(test_images, test_labels)
print("測試精確度:", test_accuracy)
