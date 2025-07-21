import subprocess
while True:
# root.txt = 這個檔案用來儲存計數器數字，根據該數字執行對應的測試腳本。
# root.py = 這個腳本(本腳本）負責讀取計數器數字，並根據該數字執行對應的測試腳本。
# test1,py = 這個腳本負責錄音，並儲存音訊資料並將錄音結果轉換為 MFCC 特徵向量。
# test2.py = .npz 檔案讀取與顯示，並顯示 MFCC 特徵向量的內容。
# test3.py = .npz 檔案讀取與顯示範例，讀取 MFCC 特徵向量並顯示為圖形。
# test4.py = 這個腳本負責讀取 .npz 檔案中的 MFCC 特徵向量，並使用隨機森林分類器進行訓練和測試。
# test5.py = 這個腳本負責將輸入的文字轉換為數字列表，並將其儲存到 wordbase.json 中。
# test6.py = 這個腳本負責選擇圖片並將其與文字和編碼數字一起儲存到 dataset_index.json 中。
# 讀取計數器數字
    with open("root.txt", "r") as f:
        counter = f.read().strip()

# 檔名組合
    filename = f"test{counter}.py"

# 執行該檔案
    subprocess.run(["python", filename])