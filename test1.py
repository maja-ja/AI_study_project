# test1.py
# 這個腳本負責錄音並儲存音訊資料，
# 並將錄音結果轉換為 MFCC 特徵向量。
# 最後將 MFCC 向量儲存為 .npz 檔
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
import librosa
import librosa.display
#import json
import datetime
import os

# === 基本參數設定 ===
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

# 在 timestamp 之前先建立 audio 資料夾
audio_folder = "audio"
os.makedirs(audio_folder, exist_ok=True)

# 自動產生時間戳檔名
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# 將 wav 檔名改成放進 audio 資料夾
WAVE_OUTPUT_FILENAME = os.path.join(audio_folder, f'audio_output_{timestamp}.wav')



# === 啟動錄音 ===
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

# === 實時波形顯示設定 ===
plt.ion()
fig, ax = plt.subplots()
x = np.arange(0, CHUNK)
line, = ax.plot(x, np.zeros(CHUNK))
ax.set_xlim(0, CHUNK)
ax.set_ylim(-32768, 32767)

# === WAV檔案寫入設定 ===
wave_output_file = wave.open(WAVE_OUTPUT_FILENAME, "wb")
wave_output_file.setnchannels(CHANNELS)
wave_output_file.setsampwidth(audio.get_sample_size(FORMAT))
wave_output_file.setframerate(RATE)

def update_plot(data):
    line.set_ydata(data)
    fig.canvas.draw()
    fig.canvas.flush_events()

# === 主錄音流程 ===
def display_audio_waveform():
    print("🎙️ 開始錄音中... 按 Ctrl+C 結束並進行分析")
    try:
        while True:
            audio_data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            update_plot(audio_data)
            wave_output_file.writeframes(audio_data.tobytes())
    except KeyboardInterrupt:
        pass  # 停止錄音後跳出迴圈
    finally:
        print("\n🛑 錄音結束，開始分析...")

        # === 結束錄音 ===
        stream.stop_stream()
        stream.close()
        audio.terminate()
        wave_output_file.close()

        # === 1. 載入音訊資料 ===
        y, sr = librosa.load(WAVE_OUTPUT_FILENAME, sr=RATE)

        # === 2. 取 MFCC 特徵向量 ===
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

        # === 3. 顯示與儲存 MFCC 圖像 ===

        # === 4. 儲存 MFCC 向量到 JSON 檔案 ===
        folder = "mfcc_files"
        os.makedirs(folder, exist_ok=True)  # 確保資料夾存在

        filename = f"mfcc_{timestamp}.npz"
        filepath = os.path.join(folder, filename)

        np.savez(filepath, mfcc=mfcc)
        print(f"MFCC 已存到 {filepath}") 

# === 執行錄音流程 ===
display_audio_waveform()
