import asyncio
import struct
import math
import numpy as np
from bleak import BleakClient
import matplotlib.pyplot as plt

# 1min,誤差0.25cm
# Global variables to hold state
record_index1 = 0
record_index2 = 1
timestamp_slot = [0,0,0,0,0,0]
first_timstamp = [0,0,0,0,0,0]
last_timestamp = [0,0,0,0,0,0]
correction = [np.array([0.0,0.0,0.0], dtype='g'),np.array([0.0,0.0,0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g')]
last_acceleration = [np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g')]
last_velocity = [np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g')]
acceleration = [np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g')]
velocity = [np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g')]
position = [np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g')]
device_address = ["D4:22:CD:00:19:02", "D4:22:CD:00:1A:4E", "D4:22:CD:00:18:FA", "D4:22:CD:00:18:F9", "D4:22:CD:00:43:33"]
timestamps = [[],[],[]]
record = [[[],[],[],[],[],[],[]],[[],[],[],[],[],[],[]],[[],[],[],[],[],[],[]]]

async def main():
    
    print("*")
    f, ax = plt.subplots(3,3)
    ax[0][0].plot(timestamps[0],record[0][0],'r:')
    ax[0][0].plot(timestamps[0],record[0][1],'g:')
    ax[0][0].plot(timestamps[0],record[0][2],'b:')
    ax[1][0].plot(timestamps[0],record[0][3],'r:')
    ax[1][0].plot(timestamps[0],record[0][4],'g:')
    ax[1][0].plot(timestamps[0],record[0][5],'b:')
    ax[2][0].plot(timestamps[0],record[0][6],'k:')
    ax[0][1].plot(timestamps[1],record[1][0],'r:')
    ax[0][1].plot(timestamps[1],record[1][1],'g:')
    ax[0][1].plot(timestamps[1],record[1][2],'b:')
    ax[1][1].plot(timestamps[1],record[1][3],'r:')
    ax[1][1].plot(timestamps[1],record[1][4],'g:')
    ax[1][1].plot(timestamps[1],record[1][5],'b:')
    ax[2][1].plot(timestamps[1],record[1][6],'k:')
    ax[0][2].plot(timestamps[2],record[2][0],'r:')
    ax[0][2].plot(timestamps[2],record[2][1],'g:')
    ax[0][2].plot(timestamps[2],record[2][2],'b:')
    ax[1][2].plot(timestamps[2],record[2][3],'r:')
    ax[1][2].plot(timestamps[2],record[2][4],'g:')
    ax[1][2].plot(timestamps[2],record[2][5],'b:')
    ax[2][2].plot(timestamps[2],record[2][6],'k:')
    plt.show()

def notification_handler(data, device_address):
    global record, record_index1, record_index2, timestamps, last_timestamp, last_acceleration, last_velocity, acceleration, velocity, position, timestamp_slot, first_timstamp
    if len(data) >= 32:
        timestamp, quaternion_w, quaternion_x, quaternion_y, quaternion_z, acceleration_x, acceleration_y, acceleration_z = struct.unpack('I7f', data[:32])
        acceleration[index] = np.array([acceleration_x, acceleration_y, acceleration_z], dtype='g') - correction[index]
        if first_timstamp[index] != 0:
            if (timestamp-first_timstamp[5])/1e6 < 5:
                return
            if abs(acceleration[index][0])<0.05:
                correction[index][0] = correction[index][0]*0.875 + acceleration_x*0.125
            if abs(acceleration[index][1])<0.05:
                correction[index][1] = correction[index][1]*0.875 + acceleration_y*0.125
            if abs(acceleration[index][2])<0.05:
                correction[index][2] = correction[index][2]*0.875 + acceleration_z*0.125
            delta_t = (timestamp - last_timestamp[index]) / 1e6  # Convert microseconds to seconds
            last_timestamp[index] = timestamp
            if (timestamp-first_timstamp[5])/1e6 < 10:
                return
            velocity[index] += 0.5 * (acceleration[index] + last_acceleration[index]) * delta_t
            position[index] += 0.5 * (velocity[index] + last_velocity[index]) * delta_t
            last_acceleration[index] = acceleration[index]
            last_velocity[index] = velocity[index]

            if index==record_index1:
                if timestamp-timestamp_slot[index]>0:
                    timestamp_slot[index]=timestamp
                    timestampdiff = (timestamp-first_timstamp[index])/1e6
                    dis = math.sqrt(position[index][0]*position[index][0]+position[index][1]*position[index][1]+position[index][2]*position[index][2])
                    print(f"Sec: {timestampdiff}")
                    timestamps[1].append(timestampdiff)
                    record[1][0].append(acceleration[index][0])
                    record[1][1].append(acceleration[index][1])
                    record[1][2].append(acceleration[index][2])
                    record[1][3].append(velocity[index][0])
                    record[1][4].append(velocity[index][1])
                    record[1][5].append(velocity[index][2])
                    record[1][6].append(dis)
            if index==record_index2:
                if timestamp-timestamp_slot[index]>0:
                    timestamp_slot[index]=timestamp
                    timestampdiff = (timestamp-first_timstamp[index])/1e6
                    dis = math.sqrt(position[index][0]*position[index][0]+position[index][1]*position[index][1]+position[index][2]*position[index][2])
                    timestamps[2].append(timestampdiff)
                    record[2][0].append(acceleration[index][0])
                    record[2][1].append(acceleration[index][1])
                    record[2][2].append(acceleration[index][2])
                    record[2][3].append(velocity[index][0])
                    record[2][4].append(velocity[index][1])
                    record[2][5].append(velocity[index][2])
                    record[2][6].append(dis)

            if index==record_index1 or index==record_index2:
                acceleration[5] = acceleration[record_index1] - acceleration[record_index2]
                velocity[5] += 0.5 * (acceleration[5] + last_acceleration[5]) * delta_t
                position[5] += 0.5 * (velocity[5] + last_velocity[5]) * delta_t
                last_acceleration[5] = acceleration[5]
                last_velocity[5] = velocity[5]
                if timestamp-timestamp_slot[5]>0:
                    timestamp_slot[5]=timestamp
                    timestampdiff = (timestamp-first_timstamp[5])/1e6
                    dis = math.sqrt(position[5][0]*position[5][0]+position[5][1]*position[5][1]+position[5][2]*position[5][2])
                    # print(f"Sec: {timestampdiff}")
                    # print(f"\nCalculate data frodiffm diff")
                    # print(f"Timestamp: {timestamp}")
                    # print(f"Quaternion: w={quaternion_w}, x={quaternion_x}, y={quaternion_y}, z={quaternion_z}")
                    # print(f"Acceleration: x={acceleration[0]}, y={acceleration[1]}, z={acceleration[2]}")
                    # print(f"Velocity: x={velocity[5][0]}, y={velocity[5][1]}, z={velocity[5][2]}")
                    # print(f"Position: x={position[5][0]}, y={position[5][1]}, z={position[5][2]}")
                    # print(f"distance to origin(m): {dis}")
                    # print(f"deviation(m/s): {dis/timestampdiff}")
                    timestamps[0].append(timestampdiff)
                    record[0][0].append(acceleration[5][0])
                    record[0][1].append(acceleration[5][1])
                    record[0][2].append(acceleration[5][2])
                    record[0][3].append(velocity[5][0])
                    record[0][4].append(velocity[5][1])
                    record[0][5].append(velocity[5][2])
                    record[0][6].append(dis)

            if timestamp-timestamp_slot[index]>0:
                timestamp_slot[index]=timestamp
                timestamp = (timestamp-first_timstamp[index])/1e6
                # print(f"\nReceived data from {device_address}")
                # print(f"Timestamp: {timestamp}")
                # print(f"Quaternion: w={quaternion_w}, x={quaternion_x}, y={quaternion_y}, z={quaternion_z}")
                # print(f"Acceleration: x={acceleration[0]}, y={acceleration[1]}, z={acceleration[2]}")
                # print(f"Velocity: x={velocity[index][0]}, y={velocity[index][1]}, z={velocity[index][2]}")
                # print(f"Position: x={position[index][0]}, y={position[index][1]}, z={position[index][2]}")
                dis = math.sqrt(position[index][0]*position[index][0]+position[index][1]*position[index][1]+position[index][2]*position[index][2])
                # print(f"distance to origin(m): {dis}")
                # print(f"deviation(m/s): {dis/timestamp}")
        else:
            first_timstamp[index] = timestamp
            last_timestamp[index] = timestamp
            correction[index][2] = acceleration[index][2]
            if first_timstamp[5] == 0:
                first_timstamp[5] = timestamp
                last_timestamp[5] = timestamp
    else:
        print("Received data is too short!")

if __name__ == "__main__":
    asyncio.run(main())
