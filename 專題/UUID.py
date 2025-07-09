import asyncio
from bleak import BleakClient

async def list_services_and_characteristics(address):
    try:
        async with BleakClient(address) as client:
            if await client.is_connected():
                print(f"已連接到設備 {address}")
                for service in client.services:
                    print(f"服務 {service.uuid}:")
                    for characteristic in service.characteristics:
                        print(f"  特徵 {characteristic.uuid}")
            else:
                print("無法連接到設備")
    except Exception as e:
        print(f"在嘗試連接或讀取服務時發生錯誤: {e}")

# 設備的藍牙地址（替換為實際地址）
device_address = "D4:22:CD:00:19:02"

# 執行該函數
loop = asyncio.get_event_loop()
loop.run_until_complete(list_services_and_characteristics(device_address))
