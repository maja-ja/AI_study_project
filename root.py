import subprocess
while True:
# root.py = 這個腳本負責讀取計數器數字，並根據該數字執行對應的測試腳本。
# test1,py = 這個腳本負責錄音，並儲存音訊資料並將錄音結果轉換為 MFCC 特徵向量。
# test2.py = .npz 檔案讀取與顯示，並顯示 MFCC 特徵向量的內容。
# test3.py = .npz 檔案讀取與顯示範例，讀取 MFCC 特徵向量並顯示為圖形。
# test4.py = 這個腳本負責讀取 .npz 檔案中的 MFCC 特徵向量，並使用隨機森林分類器進行訓練和測試。
# 讀取計數器數字
    with open("root.txt", "r") as f:
        counter = f.read().strip()

# 檔名組合
    filename = f"test{counter}.py"

# 執行該檔案
    subprocess.run(["python", filename])