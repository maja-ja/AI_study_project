import json
import os
import tkinter as tk
from tkinter import filedialog
import shutil

# 指定絕對路徑資料夾
BASE_DIR = "/Users/chenpinrong/Foxconn_Pino_study_project-2/database/word_picture"
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# 建立資料夾
os.makedirs(IMAGES_DIR, exist_ok=True)

# 建立編碼字典（ASCII 字元）
chrbase = {i: chr(i) for i in range(32, 127)}
reverse_chrbase = {v: k for k, v in chrbase.items()}

# 載入 wordbase.json，如果不存在就空字典
wordbase_path = os.path.join(BASE_DIR, "wordbase.json")
if os.path.exists(wordbase_path):
    with open(wordbase_path, "r", encoding="utf-8") as f:
        wordbase = json.load(f)
else:
    wordbase = {}

# 載入 dataset_index.json，如果不存在就空列表
dataset_index_path = os.path.join(BASE_DIR, "dataset_index.json")
if os.path.exists(dataset_index_path):
    with open(dataset_index_path, "r", encoding="utf-8") as f:
        dataset_index = json.load(f)
else:
    dataset_index = []

def encode_text(text):
    text = text.lower()
    return [reverse_chrbase[c] if c in reverse_chrbase else 0 for c in text]

def save_all():
    with open(wordbase_path, "w", encoding="utf-8") as f:
        json.dump(wordbase, f, ensure_ascii=False, indent=2)
    with open(dataset_index_path, "w", encoding="utf-8") as f:
        json.dump(dataset_index, f, ensure_ascii=False, indent=2)

def select_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="選擇一張圖片",
        filetypes=[
            ("PNG Images", "*.png"),
            ("JPEG Images", "*.jpg"),
            ("JPEG Images", "*.jpeg"),
            ("All Images", "*.png *.jpg *.jpeg")
        ]
    )
    return file_path


counter = len(dataset_index) + 1

while True:
    try:
        text = input("請輸入一句文字（Enter 離開）：").strip()
        if not text:
            break

        encoded = encode_text(text)
        wordbase[text] = encoded

        print("請選擇一張對應的圖片...")
        img_path = select_image()

        if img_path:
            img_ext = os.path.splitext(img_path)[1]
            # 避免特殊字元，檔名只留英數與底線
            safe_text = ''.join(c if c.isalnum() or c=='_' else '_' for c in text.replace(' ', '_'))
            filename = f"{counter:06d}_{safe_text}{img_ext}"
            dest_path = os.path.join(IMAGES_DIR, filename)
            shutil.copy(img_path, dest_path)

            dataset_index.append({
                "id": counter,
                "text": text,
                "vector": encoded,
                "image_path": dest_path
            })

            print(f"✅ 圖片與文字已儲存：{filename}\n")
            counter += 1
            save_all()

        else:
            print("⚠️ 未選擇圖片，跳過。")

    except KeyboardInterrupt:
        print("\n❗ 已手動結束")
        break
