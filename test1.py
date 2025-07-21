# 「字符對應數字」與「字串轉換成數字列表」的簡易轉換器
import json
import os

# 定義 chrbase：可支援所有 ASCII 可見字元
chrbase = {i: chr(i) for i in range(32, 127)}  # 空格到 ~
reverse_chrbase = {v: k for k, v in chrbase.items()}  # 快速反查

# wordbase 儲存轉換紀錄
wordbase = {}

# 讀取 wordbase.json 如果存在
if os.path.exists("wordbase.json"):
    with open("wordbase.json", "r", encoding="utf-8") as f:
        wordbase = json.load(f)

def encode_text(text):
    text = text.lower()  # 全部轉小寫
    result = []
    for c in text:
        if c in reverse_chrbase:
            result.append(reverse_chrbase[c])
        else:
            result.append(0)  # 找不到的字元設為 0
    return result

def decode_numbers(nums):
    return ''.join([chrbase.get(n, '?') for n in nums])

def save_wordbase():
    with open("wordbase.json", "w", encoding="utf-8") as f:
        json.dump(wordbase, f, ensure_ascii=False, indent=2)

print("字元轉換器啟動！輸入文字將會編碼為數字（Ctrl+C 可退出）\n")

while True:
    try:
        input_1 = input("請輸入文字： ")
        encoded = encode_text(input_1)
        decoded = decode_numbers(encoded)

        print("➡ 原始文字：", input_1)
        print("➡ 編碼數字：", encoded)
        print("➡ 還原文字：", decoded)

        wordbase[input_1] = encoded
        save_wordbase()
        print("✅ 已儲存至 wordbase.json\n")

    except KeyboardInterrupt:
        print("\n❗已退出轉換器")
        break
