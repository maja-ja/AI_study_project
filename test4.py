# test4.py
# 這個腳本負責讀取 .npz
# 檔案中的 MFCC 特徵向量，
# 並使用隨機森林分類器進行訓練和測試。
# 最後輸出測試集的準確率。
import os
import numpy as np
import librosa
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ==== 初始化 ====
X = []  # 特徵
y = []  # 標籤

data_dir = "mfcc_files"  # 結構：mfcc_files/你好/*.npz、mfcc_files/嗨/*.npz

for label in os.listdir(data_dir):
    label_dir = os.path.join(data_dir, label)
    if os.path.isdir(label_dir):
        for filename in os.listdir(label_dir):
            if filename.endswith(".npz"):
                filepath = os.path.join(label_dir, filename)
                try:
                    data = np.load(filepath)
                    mfcc = data["mfcc"]
                    mfcc_mean = np.mean(mfcc, axis=1)  # shape: (13,)
                    X.append(mfcc_mean)
                    y.append(label)
                except Exception as e:
                    print(f"❌ 無法讀取 {filepath}: {e}")

X = np.array(X)
y = np.array(y)
print(f"✅ 載入完成，共 {len(X)} 筆資料，分類有：{set(y)}")

# ==== 分割訓練/測試集 ====
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==== 建立與訓練模型 ====
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# ==== 預測與結果 ====
y_pred = clf.predict(X_test)
print("🎯 測試集準確率:", accuracy_score(y_test, y_pred))
print("y =", y)
