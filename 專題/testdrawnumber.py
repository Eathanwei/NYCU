import asyncio
import struct
import math
import numpy as np
from bleak import BleakClient
import matplotlib.pyplot as plt

# Global variables to hold state
record_index1 = 1
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
record = [[[],[],[],[],[],[],[]],[[],[],[],[],[],[],[]],[[],[],[],[],[],[],[]],[[],[],[],[],[],[],[]],[[],[],[],[],[],[],[]]]

async def control_measurement(client, action, mode):
    """Control the measurement process on the sensor."""
    control_value = bytearray([1, action, mode])  # Start measurement in a specified mode
    await client.write_gatt_char("15172001-4947-11e9-8646-d663bd873d93", control_value)
    print("Control command sent.")

async def connect_and_start(client):
    try:
        await client.connect()
        print(f"Connected to device {client.address}")
        await control_measurement(client, 1, mode=3)  # Start, Complete_Quaternion
        await client.start_notify("15172003-4947-11e9-8646-d663bd873d93", lambda sender, data: notification_handler(data, client.address))
        print(f"Notifications started for device {client.address}.")
    except Exception as e:
        print(f"Error with device {client.address}: {str(e)}")

async def stop_and_disconnect(client):
    try:
        await client.stop_notify("15172003-4947-11e9-8646-d663bd873d93")
        print(f"Notifications stopped for device {client.address}.")
    except Exception as e:
        print(f"Could not stop notifications for {client.address}: {str(e)}")
    try:
        await client.disconnect()
        print(f"Disconnected from device {client.address}")
    except Exception as e:
        print(f"Could not disconnect from {client.address}: {str(e)}")

async def main():
    client0 = BleakClient(device_address[record_index1], timeout=10.0)
    await asyncio.gather( # mode 3: Complete_Quaternion
        connect_and_start(client0),
    )
    # Listen for notifications on the long payload characteristic
    #await client.start_notify("15172003-4947-11e9-8646-d663bd873d93", notification_handler)
    # Keep the program running to receive notifications
    await asyncio.sleep(1200)  # Extend time as needed
    
    await asyncio.gather(
        stop_and_disconnect(client0),
    )
    print("*")
    f, ax = plt.subplots(3,5)
    for i in range(0,5):
        ax[0][i].plot(timestamps[record_index1],record[i][0],'r:')
        ax[0][i].plot(timestamps[record_index1],record[i][1],'g:')
        ax[0][i].plot(timestamps[record_index1],record[i][2],'b:')
        ax[1][i].plot(timestamps[record_index1],record[i][3],'r:')
        ax[1][i].plot(timestamps[record_index1],record[i][4],'g:')
        ax[1][i].plot(timestamps[record_index1],record[i][5],'b:')
        ax[2][i].plot(timestamps[record_index1],record[i][6],'k:')
    plt.show()

def notification_handler(data, device_address):
    global record, record_index1, record_index2, timestamps, last_timestamp, last_acceleration, last_velocity, acceleration, velocity, position, timestamp_slot, first_timstamp
    if len(data) >= 32:
        timestamp, quaternion_w, quaternion_x, quaternion_y, quaternion_z, acceleration_x, acceleration_y, acceleration_z = struct.unpack('I7f', data[:32])
        # print(f"Acceleration: x={acceleration[0]}, y={acceleration[1]}, z={acceleration[2]}")
        if (timestamp-first_timstamp[record_index1])/1e6 < 5:
            return
        acceleration[0] = np.array([acceleration_x, acceleration_y, acceleration_z], dtype='g')
        for index in range(1,5):
            acceleration[index] = np.array([acceleration_x, acceleration_y, acceleration_z], dtype='g') - correction[index]
            if abs(acceleration[index][0])<0.05:
                correction[index][0] = correction[index][0] + acceleration[index][0]*0.01*(index+4)
            if abs(acceleration[index][1])<0.05:
                correction[index][1] = correction[index][1] + acceleration[index][1]*0.01*(index+4)
            if abs(acceleration[index][2])<0.05:
                correction[index][2] = correction[index][2] + acceleration[index][2]*0.01*(index+4)
        if first_timstamp[record_index1] != 0:
            delta_t = (timestamp - last_timestamp[record_index1]) / 1e6  # Convert microseconds to seconds
            last_timestamp[record_index1] = timestamp
            if (timestamp-first_timstamp[record_index1])/1e6 < 10:
                return
            timestampdiff = (timestamp-first_timstamp[record_index1])/1e6
            timestamps[record_index1].append(timestampdiff)
            print(f"Sec: {timestampdiff}")
            for index in range(0,5):
                velocity[index] += 0.5 * (acceleration[index] + last_acceleration[index]) * delta_t
                position[index] += 0.5 * (velocity[index] + last_velocity[index]) * delta_t
                last_acceleration[index] = acceleration[index]
                last_velocity[index] = velocity[index]
                dis = math.sqrt(position[index][0]*position[index][0]+position[index][1]*position[index][1]+position[index][2]*position[index][2])
                record[index][0].append(acceleration[index][0])
                record[index][1].append(acceleration[index][1])
                record[index][2].append(acceleration[index][2])
                record[index][3].append(velocity[index][0])
                record[index][4].append(velocity[index][1])
                record[index][5].append(velocity[index][2])
                record[index][6].append(dis)
        else:
            for index in range(0,5):
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
