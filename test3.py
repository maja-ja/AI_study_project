# test3.py
# .npz 檔案讀取與顯示範例
# 這段程式碼會讓使用者選擇一個 .npz 檔案，
# 並讀取其中的 MFCC 特徵向量，
# 最後將其顯示為圖形。
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="選擇 .npz 檔案",
    filetypes=[("NPZ files", "*.npz")]
)

data = np.load("mfcc.npz")  # 替換為你的實際檔名
mfcc = data["arr_0"]
plt.figure(figsize=(10, 6))
for i in range(13):
    plt.plot(mfcc[i], label=f'MFCC {i}')
plt.legend()
plt.title('MFCC Features Over Time')
plt.xlabel('Frame Index')
plt.ylabel('Coefficient Value')
plt.show()


