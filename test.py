p=1
a=2
t=3
P=[a,t]
A=[p,t]
T=[p,a]
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
import librosa
import librosa.display
import matplotlib.pyplot as plt
FORMAT = pyaudio.paInt16
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate (samples per second)
CHUNK = 4096  # Number of frames per buffer
WAVE_OUTPUT_FILENAME = 'audio_output.wav'

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

# Initialize the plot for real-time waveform display
plt.ion()
fig, ax = plt.subplots()
x = np.arange(0, CHUNK)
line, = ax.plot(x, np.zeros(CHUNK))
ax.set_xlim(0, CHUNK)
ax.set_ylim(-32768, 32767)  # Assuming 16-bit audio

# Create a wave file to save the audio
wave_output_file = wave.open(WAVE_OUTPUT_FILENAME, "wb")
wave_output_file.setnchannels(CHANNELS)
wave_output_file.setsampwidth(audio.get_sample_size(FORMAT))
wave_output_file.setframerate(RATE)

def update_plot(data):
    line.set_ydata(data)
    fig.canvas.draw()
    fig.canvas.flush_events()

# Function to continuously capture and display audio
def display_audio_waveform():
    try:
        while True:
            audio_data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            update_plot(audio_data)
            wave_output_file.writeframes(audio_data.tobytes())
    except KeyboardInterrupt:
        pass

display_audio_waveform()

stream.stop_stream()
stream.close()
audio.terminate()
wave_output_file.close()
print('Audio saved to', WAVE_OUTPUT_FILENAME)


# 1. 讀入剛剛錄好的 .wav 檔
y, sr = librosa.load(WAVE_OUTPUT_FILENAME, sr=RATE)

# 2. 取 MFCC（梅爾頻率倒譜係數）
mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

# 3. 畫出 MFCC

plt.figure(figsize=(10, 4))
librosa.display.specshow(mfcc, x_axis='time')
plt.colorbar()
plt.title('MFCC')
plt.tight_layout()
plt.show()
