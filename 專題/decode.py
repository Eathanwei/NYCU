import struct

def parse_medium_payload(data):
    if len(data) < 32:  # 4 + 16 + 12 = 32 bytes for minimum expected data length
        print("Data too short to parse.")
        return

    # Unpack data according to specified format
    timestamp = struct.unpack('I', data[0:4])[0]
    quaternion_w, quaternion_x, quaternion_y, quaternion_z = struct.unpack('ffff', data[4:20])
    acceleration_x, acceleration_y, acceleration_z = struct.unpack('fff', data[20:32])

    # Display unpacked data
    print(f"Timestamp: {timestamp}")
    print(f"Quaternion: w={quaternion_w}, x={quaternion_x}, y={quaternion_y}, z={quaternion_z}")
    print(f"Acceleration: x={acceleration_x}, y={acceleration_y}, z={acceleration_z}")
    for i in range(10):
        print('[' + str(i*4) + ',' + str(i*4+4) +']: ',end='')
        print(data[i*4:i*4+4])

# Example usage with the provided bytearray
data_bytes = bytearray(b'y` \x01\xa86\xad;\x80h\x1f<\xa2;\r\xbc\x8e\xf9\x7f\xbf\xa1\xe7-\xbc\x06\xa4\x93;\x00\xdc\xcb\xbc\x00\x00\x00\x00\x00\x00\x00\x00')
parse_medium_payload(data_bytes)