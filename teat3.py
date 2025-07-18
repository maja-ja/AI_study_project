import matplotlib.pyplot as plt
import numpy as np
data = np.load("mfcc.npz")  # 替換為你的實際檔名
mfcc = data["arr_0"]
plt.figure(figsize=(10, 6))
for i in range(13):
    plt.plot(mfcc[i], label=f'MFCC {i}')
plt.legend()
plt.title('MFCC Features Over Time')
plt.xlabel('Frame Index')
plt.ylabel('Coefficient Value')
plt.show()


