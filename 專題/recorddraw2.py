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

dt = 0.1
A = np.array([[1, dt, 0.5 * dt**2],
              [0, 1, dt],
              [0, 0, 1]])
H = np.array([[0, 0, 1]])
Q = np.array([[1e-5, 0, 0],
              [0, 1e-5, 0],
              [0, 0, 1e-5]])
R = np.array([[0.01]])

def kalman_filter(measurements):
    x = np.array([[0], [0], [0]])
    P = np.eye(3)
    estimated_states = []
    previous_timestamp = timestamps[0]
    for i, z in enumerate(measurements):
        current_timestamp = timestamps[i]
        dt = current_timestamp - previous_timestamp
        previous_timestamp = current_timestamp
        A = np.array([[1, dt, 0.5 * dt**2],
                    [0, 1, dt],
                    [0, 0, 1]])
        x = np.dot(A, x)
        P = np.dot(A, np.dot(P, A.T)) + Q
        S = np.dot(H, np.dot(P, H.T)) + R
        K = np.dot(P, np.dot(H.T, np.linalg.inv(S)))
        y = z - np.dot(H, x)
        x = x + np.dot(K, y)
        P = P - np.dot(K, np.dot(H, P))
        estimated_states.append(x.flatten())
    return np.array(estimated_states)

start_index = next(i for i, t in enumerate(timestamps) if t > 5)
filtered_x = kalman_filter(count_x[start_index:])
filtered_y = kalman_filter(count_y[start_index:])
filtered_z = kalman_filter(count_z[start_index:])

filtered_data = pd.DataFrame({
    'filtered_x': filtered_x[:, 2],
    'filtered_y': filtered_y[:, 2],
    'filtered_z': filtered_z[:, 2]
})
filtered_data.to_csv('filtered_acceleration_data.csv', index=False)

print("*")
f, ax = plt.subplots(3,2)
ax[0][0].plot(timestamps[start_index:],acc_x[start_index:],'r:')
ax[0][0].plot(timestamps[start_index:],acc_y[start_index:],'g:')
ax[0][0].plot(timestamps[start_index:],acc_z[start_index:],'b:')
ax[1][0].plot(timestamps[start_index:],np.cumsum(acc_x[start_index:]) * np.mean(np.diff(timestamps)),'r:')
ax[1][0].plot(timestamps[start_index:],np.cumsum(acc_y[start_index:]) * np.mean(np.diff(timestamps)),'g:')
ax[1][0].plot(timestamps[start_index:],np.cumsum(acc_z[start_index:]) * np.mean(np.diff(timestamps)),'b:')
ax[2][0].plot(timestamps[start_index:],np.cumsum(np.cumsum(acc_x[start_index:])) * np.mean(np.diff(timestamps))**2,'r:')
ax[2][0].plot(timestamps[start_index:],np.cumsum(np.cumsum(acc_y[start_index:])) * np.mean(np.diff(timestamps))**2,'g:')
ax[2][0].plot(timestamps[start_index:],np.cumsum(np.cumsum(acc_z[start_index:])) * np.mean(np.diff(timestamps))**2,'b:')
ax[0][1].plot(timestamps[start_index:],filtered_x[:, 2],'r:')
ax[0][1].plot(timestamps[start_index:],filtered_y[:, 2],'g:')
ax[0][1].plot(timestamps[start_index:],filtered_z[:, 2],'b:')
ax[1][1].plot(timestamps[start_index:],filtered_x[:, 1],'r:')
ax[1][1].plot(timestamps[start_index:],filtered_y[:, 1],'g:')
ax[1][1].plot(timestamps[start_index:],filtered_z[:, 1],'b:')
ax[2][1].plot(timestamps[start_index:],filtered_x[:, 0],'r:')
ax[2][1].plot(timestamps[start_index:],filtered_y[:, 0],'g:')
ax[2][1].plot(timestamps[start_index:],filtered_z[:, 0],'b:')
plt.show()