# part_1.py
# 這段程式碼是 maja-ja（GitHub 初學者）學習機器學習的一部分。
# ----------- 簡單的函數 y = w * x + b ----------------
# 這個函數用來計算一個簡單線性模型的輸出。
# w 和 b 可以改變，而 x 是固定的。
# 如果我們令 theta = [w, b]，那麼我們可以將函數寫成：
# f_theta(x) = w * x + b，例如：
# f_theta(3) = 2 * x + 1，其中 theta[w, b] = [2, 1]
# ----------- 損失函數（Loss function） ------------------------
# 通常，損失函數用來衡量模型的表現好壞。
# L = Σ((y[i] - y_hat[i])^2)    
# 其中：
# (y[i] - y_hat[i]) 是真實輸出 y[i] 與預測輸出 y_hat[i] 之間的誤差
# 這個函數用來計算每一筆輸入資料的誤差
# 在 Python 中可以寫成：
# L = sum((y[i] - y_hat[i])**2 for i in range(len(y)))
# L = sum((a - b)**2 for a, b in zip(y, y_hat)) # 更 Pythonic 的寫法
# ----------- 學習的函數模型 ------------------                                                    
# Σ(w[i] * x[i]) + b[1] = w[1]*x[1] + w[2]*x[2] + w[3]*x[3] <---- 激活函數（activation function）
# 其中：                
# x[i] = 輸入值（固定不可變）  
# w[i] = 權重值（可以調整）  
# b[1] = 偏差值（可以調整）  
# Σ = 激活函數  
# w[i] 和 b[1] 是模型中需要學習的參數  
# 學習的目標就是找到一組最好的 w[i] 和 b[1] 值，使得損失函數 L 最小  
# ------------ 如何學習（how to learn） -------------------
# Python 中簡單線性模型 y = w * x + b 的實作方式如下：

def linear_model(x, theta):
    w, b = theta
    return w * x + b

# 第一組測試資料
x_values = [1, 2, 3]  # 輸入值
y_true = [3, 5, 7]    # 真實輸出值
theta = [2, 1]        # w=2, b=1 → 目標模型為 y = 2x + 1

y_hat = [linear_model(x, theta) for x in x_values]  # 預測值
loss = sum((y - y_pred)**2 for y, y_pred in zip(y_true, y_hat))  # 計算損失
print(f"Loss: {loss}")  # 如果模型完美，Loss 應為 0

# 第二組測試資料（改變了輸入）
x_values = [1, 3, 5]  # 輸入值（不同於第一組）
y_true = [3, 5, 7]    # 真實輸出值
theta = [2, 1]        # 仍然是 y = 2x + 1 的模型

y_hat = [linear_model(x, theta) for x in x_values]  # 預測值
loss = sum((y - y_pred)**2 for y, y_pred in zip(y_true, y_hat))  # 再次計算損失
print(f"Loss: {loss}")  # 這次的 Loss 應該不為 0，因為輸入和模型不完全吻合
