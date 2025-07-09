import asyncio
import struct
import math
import numpy as np
from bleak import BleakClient

# Global variables to hold state
times = 0
sum = np.array([0.0,0.0,0.0], dtype='g')
timestamp_slot = [0,0,0,0,0,0]
first_timstamp = [0,0,0,0,0,0]
last_timestamp = [0,0,0,0,0,0]
correction = [np.array([0.0,0.0,0.0233], dtype='g'),np.array([0.0,0.0,-0.043], dtype='g')]
last_acceleration = [np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g')]
last_velocity = [np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g')]
acceleration = [np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g')]
velocity = [np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g')]
position = [np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g'),np.array([0.0, 0.0, 0.0], dtype='g')]
device_address = ["D4:22:CD:00:19:02", "D4:22:CD:00:1A:4E", "D4:22:CD:00:18:FA", "D4:22:CD:00:18:F9", "D4:22:CD:00:43:33"]

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
    client0 = BleakClient(device_address[0], timeout=10.0)
    client1 = BleakClient(device_address[1], timeout=10.0)
    await asyncio.gather( # mode 3: Complete_Quaternion
        connect_and_start(client0),
        connect_and_start(client1)
    )
    # Listen for notifications on the long payload characteristic
    #await client.start_notify("15172003-4947-11e9-8646-d663bd873d93", notification_handler)
    # Keep the program running to receive notifications
    await asyncio.sleep(1200)  # Extend time as needed
    
    await asyncio.gather(
        stop_and_disconnect(client0),
        stop_and_disconnect(client1)
    )

def notification_handler(data, device_address):
    global times, sum, last_timestamp, last_acceleration, last_velocity, acceleration, velocity, position, timestamp_slot, first_timstamp
    if len(data) >= 32:
        timestamp, quaternion_w, quaternion_x, quaternion_y, quaternion_z, acceleration_x, acceleration_y, acceleration_z = struct.unpack('I7f', data[:32])
        # print(f"Acceleration: x={acceleration[0]}, y={acceleration[1]}, z={acceleration[2]}")
        if device_address=="D4:22:CD:00:19:02":
            index=0
        elif device_address=="D4:22:CD:00:1A:4E":
            index=1
            times += 1
            sum += np.array([acceleration_x, acceleration_y, acceleration_z], dtype='g')+correction[index]
            if timestamp-timestamp_slot[index]>1000000:
                print(f"average: {sum/times}")
        elif device_address=="D4:22:CD:00:18:FA":
            index=2
        elif device_address=="D4:22:CD:00:18:F9":
            index=3
        elif device_address=="D4:22:CD:00:43:33":
            index=4
        acceleration[index] = np.array([acceleration_x, acceleration_y, acceleration_z], dtype='g')
        if last_timestamp[index] != 0:
            delta_t = (timestamp - last_timestamp[index]) / 1e6  # Convert microseconds to seconds
            last_timestamp[index] = timestamp
            velocity[index] += 0.5 * (acceleration[index] + last_acceleration[index]) * delta_t
            position[index] += 0.5 * (velocity[index] + last_velocity[index]) * delta_t
            last_acceleration[index] = acceleration[index]
            last_velocity[index] = velocity[index]

            if index==0:
                acceleration[5] = acceleration[0] - acceleration[1]
                velocity[5] += 0.5 * (acceleration[5] + last_acceleration[5]) * delta_t
                position[5] += 0.5 * (velocity[5] + last_velocity[5]) * delta_t
                last_acceleration[5] = acceleration[5]
                last_velocity[5] = velocity[5]
                timestampdiff = timestamp
                if timestampdiff-timestamp_slot[5]>1000000:
                    timestamp_slot[5]=timestampdiff
                    timestampdiff = (timestampdiff-first_timstamp[5])/1e6
                    print(f"\nCalculate data from diff")
                    print(f"Timestamp: {timestampdiff}")
                    # print(f"Quaternion: w={quaternion_w}, x={quaternion_x}, y={quaternion_y}, z={quaternion_z}")
                    # print(f"Acceleration: x={acceleration[0]}, y={acceleration[1]}, z={acceleration[2]}")
                    print(f"Velocity: x={velocity[5][0]}, y={velocity[5][1]}, z={velocity[5][2]}")
                    print(f"Position: x={position[5][0]}, y={position[5][1]}, z={position[5][2]}")
                    dis = math.sqrt(position[5][0]*position[5][0]+position[5][1]*position[5][1]+position[5][2]*position[5][2])
                    print(f"distance to origin(m): {dis}")
                    print(f"deviation(m/s): {dis/timestampdiff}")

            if timestamp-timestamp_slot[index]>1000000:
                timestamp_slot[index]=timestamp
                timestamp = (timestamp-first_timstamp[index])/1e6
                print(f"\nReceived data from {device_address}")
                print(f"Timestamp: {timestamp}")
                # print(f"Quaternion: w={quaternion_w}, x={quaternion_x}, y={quaternion_y}, z={quaternion_z}")
                # print(f"Acceleration: x={acceleration[0]}, y={acceleration[1]}, z={acceleration[2]}")
                print(f"Velocity: x={velocity[index][0]}, y={velocity[index][1]}, z={velocity[index][2]}")
                print(f"Position: x={position[index][0]}, y={position[index][1]}, z={position[index][2]}")
                dis = math.sqrt(position[index][0]*position[index][0]+position[index][1]*position[index][1]+position[index][2]*position[index][2])
                print(f"distance to origin(m): {dis}")
                print(f"deviation(m/s): {dis/timestamp}")
        else:
            first_timstamp[index] = timestamp
            last_timestamp[index] = timestamp
            if first_timstamp[5]==0:
                first_timstamp[5] = timestamp
    else:
        print("Received data is too short!")

if __name__ == "__main__":
    asyncio.run(main())
