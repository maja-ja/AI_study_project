# test2.py
# 這個腳本負責讀取 test1.py 的 .npz 輸出，
# 並顯示 MFCC 特徵向量的內容。
import numpy as np
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="選擇 .npz 檔案",
    filetypes=[("NPZ files", "*.npz")]
)

if file_path:
    data = np.load(file_path)
    keys = list(data.keys())
    print("讀取成功！內容 key：", keys)

    mfcc = data[keys[0]]
    print(mfcc.shape) 
    data.close()
else:
    print("沒有選擇檔案")
