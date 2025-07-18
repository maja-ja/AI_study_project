import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
import librosa
import librosa.display
import json
import datetime

# === 基本參數設定 ===
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

# 自動產生時間戳檔名
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
WAVE_OUTPUT_FILENAME = f'audio_output_{timestamp}.wav'
MFCC_IMAGE_FILENAME = f'mfcc_output_{timestamp}.png'
MFCC_JSON_FILENAME = f'A_memory_{timestamp}.json'

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
        plt.ioff()
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(mfcc, x_axis='time')
        plt.colorbar()
        plt.title('MFCC')
        plt.tight_layout()
        plt.savefig(MFCC_IMAGE_FILENAME)
        plt.show()
        plt.close()

        # === 4. 儲存 MFCC 向量到 JSON 檔案 ===
        with open(MFCC_JSON_FILENAME, "w") as f:
            json.dump(mfcc.tolist(), f)

        print(f"✅ 音訊已儲存：{WAVE_OUTPUT_FILENAME}")
        print(f"✅ MFCC 圖已儲存：{MFCC_IMAGE_FILENAME}")
        print(f"✅ MFCC 向量已儲存：{MFCC_JSON_FILENAME}")

# === 執行錄音流程 ===
display_audio_waveform()
