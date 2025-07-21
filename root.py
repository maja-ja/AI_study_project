import subprocess
while True:
# root.txt = 這個檔案用來儲存計數器數字，根據該數字執行對應的測試腳本。
# root.py = 這個腳本(本腳本）負責讀取計數器數字，並根據該數字執行對應的測試腳本。
# test1,py = 這個腳本負責將輸入的文字轉換為數字列表，並將其儲存到 wordbase.json 中。
# test2.py = 這個腳本負責選擇圖片並將其與文字和編碼數字一起儲存到 dataset_index.json 中。
# 讀取計數器數字
    with open("root.txt", "r") as f:
        counter = f.read().strip()

# 檔名組合
    filename = f"test{counter}.py"

# 執行該檔案
    subprocess.run(["python", filename])