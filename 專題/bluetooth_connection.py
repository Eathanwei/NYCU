import asyncio
from bleak import BleakClient

async def connect_and_read(address):
    async with BleakClient(address) as client:
        if await client.is_connected():
            print(f"已連接到 {address}")
            # 例子：要讀取的特徵的 UUID
            uuid = "15172002-4947-11e9-8646-d663bd873d93"
            value = await client.read_gatt_char(uuid)
            print(f"特徵值：{value}")
            uuid = "15172003-4947-11e9-8646-d663bd873d93"
            value = await client.read_gatt_char(uuid)
            print(f"特徵值：{value}")
            uuid = "15172004-4947-11e9-8646-d663bd873d93"
            value = await client.read_gatt_char(uuid)
            print(f"特徵值：{value}")

# 指定你的 BLE 設備的地址
device_address = "D4:22:CD:00:19:02"
# Device Movella DOT: D4:22:CD:00:19:02
# Device Movella DOT: D4:22:CD:00:1A:4E
# Device Movella DOT: D4:22:CD:00:18:FA
# Device Movella DOT: D4:22:CD:00:18:F9
# Device Movella DOT: D4:22:CD:00:43:33
loop = asyncio.get_event_loop()
loop.run_until_complete(connect_and_read(device_address))
# Service 00001800-0000-1000-8000-00805f9b34fb - Generic Access Profile
#         Characteristic 00002a00-0000-1000-8000-00805f9b34fb - Device Name
#         Characteristic 00002a01-0000-1000-8000-00805f9b34fb - Appearance
#         Characteristic 00002a04-0000-1000-8000-00805f9b34fb - Peripheral Preferred Connection Parameters
#         Characteristic 00002aa6-0000-1000-8000-00805f9b34fb - Central Address Resolution
# Service 00001801-0000-1000-8000-00805f9b34fb - Generic Attribute Profile
#         Characteristic 00002a05-0000-1000-8000-00805f9b34fb - Service Changed
#                 Descriptor 00002902-0000-1000-8000-00805f9b34fb - Client Characteristic Configuration
# Service 15173000-4947-11e9-8646-d663bd873d93 - Unknown
#         Characteristic 15173001-4947-11e9-8646-d663bd873d93 - Battery
#                 Descriptor 00002902-0000-1000-8000-00805f9b34fb - Client Characteristic Configuration
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
# Service 15174000-4947-11e9-8646-d663bd873d93 - Unknown
#         Characteristic 15174001-4947-11e9-8646-d663bd873d93 - Reserved
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
#         Characteristic 15174002-4947-11e9-8646-d663bd873d93 - Reserved
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
#         Characteristic 15174003-4947-11e9-8646-d663bd873d93 - Reserved
#                 Descriptor 00002902-0000-1000-8000-00805f9b34fb - Client Characteristic Configuration
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
# Service 15172000-4947-11e9-8646-d663bd873d93 - Unknown
#         Characteristic 15172001-4947-11e9-8646-d663bd873d93 - Control
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
#         Characteristic 15172002-4947-11e9-8646-d663bd873d93 - Long payload length
#                 Descriptor 00002902-0000-1000-8000-00805f9b34fb - Client Characteristic Configuration
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
#         Characteristic 15172003-4947-11e9-8646-d663bd873d93 - Medium payload length
#                 Descriptor 00002902-0000-1000-8000-00805f9b34fb - Client Characteristic Configuration
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
#         Characteristic 15172004-4947-11e9-8646-d663bd873d93 - Short payload length
#                 Descriptor 00002902-0000-1000-8000-00805f9b34fb - Client Characteristic Configuration
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
#         Characteristic 15172005-4947-11e9-8646-d663bd873d93 - Reserved
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
#         Characteristic 15172006-4947-11e9-8646-d663bd873d93 - Orientation reset control
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
#         Characteristic 15172007-4947-11e9-8646-d663bd873d93 - Orientation reset status
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
#         Characteristic 15172008-4947-11e9-8646-d663bd873d93 - Orientation reset data
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
# Service 15171000-4947-11e9-8646-d663bd873d93 - Unknown
#         Characteristic 15171001-4947-11e9-8646-d663bd873d93 - Device info
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
#         Characteristic 15171002-4947-11e9-8646-d663bd873d93 - Device control
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
#         Characteristic 15171004-4947-11e9-8646-d663bd873d93 - Device report
#                 Descriptor 00002902-0000-1000-8000-00805f9b34fb - Client Characteristic Configuration
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
# Service 15177000-4947-11e9-8646-d663bd873d93 - Unknown
#         Characteristic 15177001-4947-11e9-8646-d663bd873d93 - Control
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
#         Characteristic 15177002-4947-11e9-8646-d663bd873d93 - Acknowledge
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description
#         Characteristic 15177003-4947-11e9-8646-d663bd873d93 - Notification
#                 Descriptor 00002902-0000-1000-8000-00805f9b34fb - Client Characteristic Configuration
#                 Descriptor 00002901-0000-1000-8000-00805f9b34fb - Characteristic User Description