import numpy as np
data = np.load("mfcc.npz")  # 替換為你的實際檔名
mfcc = data["arr_0"]
print(mfcc.shape)  # 通常會是 (13, N)，13 個 MFCC 向量，N 為時間步數
