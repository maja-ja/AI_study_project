import json
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import shutil

# 資料夾設定（根目錄）
BASE_DIR = "/Users/chenpinrong/Foxconn_Pino_study_project-2/database/"
WORD_NUMBER_DIR = os.path.join(BASE_DIR, "word_number")
DATASET_DIR = os.path.join(BASE_DIR, "word_picture")
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
PATH_DIR = os.path.join("/Users/chenpinrong/Foxconn_Pino_study_project-2/path")

# 建立必要資料夾
os.makedirs(WORD_NUMBER_DIR, exist_ok=True)
os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(PATH_DIR, exist_ok=True)

# 路徑設定
WORD_BASE_PATH = os.path.join(WORD_NUMBER_DIR, "wordbase.json")
DATASET_INDEX_PATH = os.path.join(DATASET_DIR, "dataset_index.json")

# 建立 ASCII 編碼表
chrbase = {i: chr(i) for i in range(32, 127)}
reverse_chrbase = {v: k for k, v in chrbase.items()}

# 載入 wordbase
if os.path.exists(WORD_BASE_PATH):
    with open(WORD_BASE_PATH, "r", encoding="utf-8") as f:
        wordbase = json.load(f)
else:
    wordbase = {}

# 載入圖文配對索引
if os.path.exists(DATASET_INDEX_PATH):
    with open(DATASET_INDEX_PATH, "r", encoding="utf-8") as f:
        dataset_index = json.load(f)
else:
    dataset_index = []

# 編碼與解碼函式
def encode_text(text: str):
    text = text.lower()
    return [reverse_chrbase.get(c, 0) for c in text]

def decode_numbers(nums):
    return ''.join([chrbase.get(n, '?') for n in nums])

# 儲存函式
def save_wordbase():
    with open(WORD_BASE_PATH, "w", encoding="utf-8") as f:
        json.dump(wordbase, f, ensure_ascii=False, indent=2)

def save_dataset_index():
    with open(DATASET_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset_index, f, ensure_ascii=False, indent=2)

# 圖片選擇
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

# 新增資料流程
def add_new_entry():
    global counter
    try:
        text = input("請輸入一句文字（Enter 離開）：").strip()
        if not text:
            return False

        encoded = encode_text(text)
        wordbase[text] = encoded

        print("請選擇一張對應的圖片...")
        img_path = select_image()

        if img_path:
            img_ext = os.path.splitext(img_path)[1]
            filename_base = f"{counter:06d}_{text.replace(' ', '_')}"
            image_filename = filename_base + img_ext
            dest_path = os.path.join(IMAGES_DIR, image_filename)
            shutil.copy(img_path, dest_path)

            # 儲存圖片與文字對應資訊
            dataset_index.append({
                "id": counter,
                "text": text,
                "vector": encoded,
                "image_path": dest_path
            })

            # 建立空白路徑檔案
            path_filename = filename_base + "_path.json"
            path_path = os.path.join(PATH_DIR, path_filename)
            with open(path_path, "w", encoding="utf-8") as f:
                json.dump([], f)  # 初始為空

            print(f"✅ 圖片與文字已儲存：{image_filename}")
            print(f"📝 空路徑檔已建立：{path_filename}\n")

            counter += 1
            save_wordbase()
            save_dataset_index()
        else:
            print("⚠️ 未選擇圖片，跳過。")
        return True

    except KeyboardInterrupt:
        print("\n❗ 已手動結束")
        return False

# 主程式
def main():
    global counter
    counter = len(dataset_index) + 1
    print("=== 字元轉換器 + 圖片配對器 ===")
    while True:
        cont = add_new_entry()
        if not cont:
            break
    print("🛑 程式結束。")

if __name__ == "__main__":
    main()
