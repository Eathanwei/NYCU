import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class ExponentialMovingAverage:
    def __init__(self, alpha):
        self.alpha = alpha
        self.ema = None
    
    def update(self, value):
        if self.ema is None:
            self.ema = value
        else:
            self.ema = self.alpha * value + (1 - self.alpha) * self.ema
        return self.ema

class KalmanFilter:
    def __init__(self, A, B, Q, P, x0):
        self.A = A
        self.B = B
        self.Q = Q
        self.P = P
        self.x = x0
    
    def predict(self, u=0):
        self.x = np.dot(self.A, self.x) + np.dot(self.B, u)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        return self.x
    
    def update(self, z, R):
        S = self.P + R
        K = self.P / S
        self.x = self.x + K * (z - self.x)
        self.P = (1 - K) * self.P
        return self.x

# 假設你有時間戳和三個軸的加速度數據
data = pd.read_csv('Movella DOT.csv')
SampleTimeFine = data['SampleTimeFine'].values
timestamps = (SampleTimeFine - SampleTimeFine[0])/1000000
acc_x = data['Acc_X'].values
acc_y = data['Acc_Y'].values
acc_z = data['Acc_Z'].values

# 初始化指數加權平均 (EMA)
alpha = 0.125  # 調整平滑參數
ema_x = ExponentialMovingAverage(alpha)
ema_y = ExponentialMovingAverage(alpha)
ema_z = ExponentialMovingAverage(alpha)

# 卡爾曼濾波器參數
A = np.array([[1]])  # 狀態轉移矩陣
B = np.array([[0]])  # 控制矩陣 (無控制輸入)
Q = np.array([[0.001]])  # 過程噪聲協方差
P = np.array([[1]])  # 初始誤差協方差
R = np.array([[0.1]])  # 觀測噪聲協方差 (這個可以調整)

# 初始化卡爾曼濾波器
kf_x = KalmanFilter(A, B, Q, P, np.array(acc_x[0]))
kf_y = KalmanFilter(A, B, Q, P, np.array(acc_y[0]))
kf_z = KalmanFilter(A, B, Q, P, np.array(acc_z[0]))

# 存儲處理後的加速度數據
smoothed_data_x = []
smoothed_data_y = []
smoothed_data_z = []
count_x = []
count_y = []
count_z = []

# 對每個時間戳和對應的三個軸數據進行處理
for i in range(len(timestamps)):
    # EMA 預測新值
    ema_pred_x = ema_x.update(acc_x[i])
    ema_pred_y = ema_y.update(acc_y[i])
    ema_pred_z = ema_z.update(acc_z[i])
    
    count_x.append(acc_x[i] - ema_pred_x)
    count_y.append(acc_y[i] - ema_pred_y)
    count_z.append(acc_z[i] - ema_pred_z)

    # 使用卡爾曼濾波器處理噪聲
    kalman_pred_x = kf_x.update(count_x[i], R)
    kalman_pred_y = kf_y.update(count_y[i], R)
    kalman_pred_z = kf_z.update(count_z[i], R)
    
    # 保存處理結果
    smoothed_data_x.append(kalman_pred_x[0])
    smoothed_data_y.append(kalman_pred_y[0])
    smoothed_data_z.append(kalman_pred_z[0])

# 定義簡單的數字積分方法（梯形積分法）
def integrate(acceleration):
    velocity = [0]  # 初始速度假設為 0
    for i in range(1, len(acceleration)):
        if timestamps[i]>0:
            delta_t = timestamps[i] - timestamps[i - 1]
            # 使用梯形積分法來計算速度
            v = velocity[i-1] + 0.5 * (acceleration[i] + acceleration[i - 1]) * delta_t
            velocity.append(v[0])
        else:
            velocity.append(0)
    return velocity

def calculate_position(velocity):
    position = [0]  # 初始位置假設為 0
    for i in range(1, len(velocity)):
        if timestamps[i]>0:
            delta_t = timestamps[i] - timestamps[i - 1]
            # 使用梯形積分法來計算位置
            p = position[i-1] + 0.5 * (velocity[i] + velocity[i - 1]) * delta_t
            position.append(p)
        else:
            position.append(0)
    return position


# 計算速度和位置
velocity_x = integrate(smoothed_data_x)
velocity_y = integrate(smoothed_data_y)
velocity_z = integrate(smoothed_data_z)
position_x = calculate_position(velocity_x)
position_y = calculate_position(velocity_y)
position_z = calculate_position(velocity_z)
start_index = next(i for i, t in enumerate(timestamps) if t > 10)
plt.figure(figsize=(12, 8))

# 繪製加速度變化圖
plt.subplot(3, 1, 1)
plt.plot(timestamps[start_index:], smoothed_data_x[start_index:], color='r')
plt.plot(timestamps[start_index:], smoothed_data_y[start_index:], color='g')
plt.plot(timestamps[start_index:], smoothed_data_z[start_index:], color='b')
plt.legend()
plt.grid(True)

# 繪製速度變化圖
plt.subplot(3, 1, 2)
plt.plot(timestamps[start_index:], velocity_x[start_index:], color='r')
plt.plot(timestamps[start_index:], velocity_y[start_index:], color='g')
plt.plot(timestamps[start_index:], velocity_z[start_index:], color='b')
plt.legend()
plt.grid(True)

# 繪製位置變化圖
plt.subplot(3, 1, 3)
plt.plot(timestamps[start_index:], position_x[start_index:], color='r')
plt.plot(timestamps[start_index:], position_y[start_index:], color='g')
plt.plot(timestamps[start_index:], position_z[start_index:], color='b')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()