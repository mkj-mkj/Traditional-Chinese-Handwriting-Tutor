# -*- coding: utf-8 -*-
import zipfile
import pandas as pd
from PIL import Image
import numpy as np
import os
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import tensorflow.keras.layers as layers
from sklearn.utils.class_weight import compute_class_weight
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter
from PIL import Image
import numpy as np
from tensorflow.keras.utils import to_categorical


# 確認是否檢測到GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"Found GPU: {gpus}")
    except RuntimeError as e:
        print(e)
else:
    print("No GPU found. Please ensure you have installed CUDA and cuDNN correctly.")

# 讀取CSV文件
data = pd.read_csv("./hanzi_label.csv")

# 打亂資料
data = data.sample(frac=1).reset_index(drop=True)



# 將字串標籤轉換為整數標籤
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(data['label'])

# 檢查原始資料集類別分布
print("原始資料集個類別樣本數:", Counter(labels_encoded))

# 定義目標樣本數量範圍
min_samples = 6000
max_samples = 12000

# 定義oversampling策略，使每個類別的樣本數至少達到 min_samples
over_sampler = RandomOverSampler(sampling_strategy={label: max(min_samples, count) for label, count in Counter(labels_encoded).items()})

# 進行oversampling
X_resampled, y_resampled = over_sampler.fit_resample(data[['filename']], labels_encoded)

# 定義undersampling策略，使每個類別的樣本數最多達到 max_samples
under_sampler = RandomUnderSampler(sampling_strategy={label: min(max_samples, count) for label, count in Counter(y_resampled).items()})

# 進行undersampling
X_resampled, y_resampled = under_sampler.fit_resample(X_resampled, y_resampled)

# 把原始資料集切割為訓練集、驗證集、測試集(8:1:1)

X_train_val, X_test, y_train_val, y_test = train_test_split(X_resampled, y_resampled, test_size=0.1, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.1/0.9, random_state=42)

# 輸出樣本數和各類別樣本數
print(f"訓練集樣本數： {X_train.shape[0]}")
print(f"驗證集樣本數： {X_val.shape[0]}")
print(f"測試集樣本數： {X_test.shape[0]}")

train_counter = Counter(y_train)
val_counter = Counter(y_val)
test_counter = Counter(y_test)

print("訓練集各類別樣本數：", train_counter)
print("驗證集各類別樣本數：", val_counter)
print("測試集各類別樣本數：", test_counter)

# 載入和預處裡影像
image_directory = './cleaned_data(50_50)'  # 資料集路徑

# 定義圖像預處理函數
def preprocess_image(image_path, target_size=(200, 200)):
    try:
        with Image.open(image_path) as img:
            img = img.resize(target_size)
            img = np.array(img)
            if img.shape[2] == 4:
                img = img[..., :3]
            img = img / 255.0
        return img
    except IOError:
        print(f"Error in opening image file {image_path}")
        return None

# 載入和預處理訓練集影像
train_images = []
train_labels = []

for filename, label in zip(X_train['filename'], y_train):
    file_path = os.path.join(image_directory, filename)
    image = preprocess_image(file_path)
    if image is not None:
        train_images.append(image)
        train_labels.append(label)

X_train_images = np.array(train_images)
y_train = np.array(train_labels)

# 載入和預處理驗證集影像
val_images = []
val_labels = []
for filename, label in zip(X_val['filename'], y_val):
    file_path = os.path.join(image_directory, filename)
    image = preprocess_image(file_path)
    if image is not None:
        val_images.append(image)
        val_labels.append(label)

X_val_images = np.array(val_images)
y_val = np.array(val_labels)

# 載入和預處理測試集影像
test_images = []
test_labels = []
for filename, label in zip(X_test['filename'], y_test):
    file_path = os.path.join(image_directory, filename)
    image = preprocess_image(file_path)
    if image is not None:
        test_images.append(image)
        test_labels.append(label)

X_test_images = np.array(test_images)
y_test = np.array(test_labels)

# 轉換標籤為分類格式
num_classes = len(np.unique(y_resampled))
y_train = to_categorical(y_train, num_classes=num_classes)
y_val = to_categorical(y_val, num_classes=num_classes)
y_test = to_categorical(y_test, num_classes=num_classes)

# 輸出圖像、標籤shape
print(f"訓練集影像的shape： {X_train_images.shape}")
print(f"驗證集影像的shape： {X_val_images.shape}")
print(f"測試集影像的shape： {X_test_images.shape}")
print(f"訓練集標籤的shape： {y_train.shape}")
print(f"驗證集標籤的shape： {y_val.shape}")
print(f"測試集標籤的shape： {y_test.shape}")

# 計算各類別權重
class_weights = compute_class_weight('balanced', classes=np.unique(y_resampled), y=y_resampled)
class_weights = {i : class_weights[i] for i in range(len(class_weights))}

# 輸出各類別權重
print("類別權重：", class_weights)


# 定義模型
model = tf.keras.models.Sequential([
    #輸入層和第一層卷積層
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(200, 200, 3)),
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
    layers.Dense(8, activation='softmax')
])


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

train_datagen = ImageDataGenerator()
val_datagen = ImageDataGenerator()

train_generator = train_datagen.flow(X_train_images, y_train, batch_size=32)  
val_generator = val_datagen.flow(X_val_images, y_val, batch_size=32)          

# 訓練模型
history = model.fit(train_generator, epochs=20, validation_data=val_generator, class_weight=class_weights)


# 用測試集評估模型
test_generator = val_datagen.flow(X_test_images, y_test, batch_size=32)
test_loss, test_accuracy = model.evaluate(test_generator)
print(f"測試集損失： {test_loss}")
print(f"測試集準確度： {test_accuracy}")

model.save('./cnn_hanzi_classifier.h5')

# def hanzi_predict(img):
#     result = ""
#     img_expanded = np.expand_dims(img, axis=0)
#     predictions = model.predict(img_expanded)
#     predicted_class_index = np.argmax(predictions, axis=1)[0]
#     author_name = rev_class_name[predicted_class_index]

#     return result