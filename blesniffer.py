import asyncio
from bleak import BleakScanner, BLEDevice, AdvertisementData, BleakClient

DEVICE_NAME = "BT05"
SERVICE_UUID = "0000ffe0-0000-1000-8000-00805F9B34FB"
CHAR_UUID = "0000ffe1-0000-1000-8000-00805F9B34FB"

def getDeviceDataFromDevice(device):
    bledevice: BLEDevice
    advdata: AdvertisementData

    bledevice, advdata = device

    d = {
        "device": bledevice,
        "name": bledevice.name,
        "details": bledevice.details,
        "address": bledevice.address,
        "local_name": advdata.local_name,
        "manufacturer_data": advdata.manufacturer_data,
        "platform_data": advdata.platform_data,
        "rssi": advdata.rssi,
        "service_data": advdata.service_data,
        "service_uuids": advdata.service_uuids,
        "tx_power": advdata.tx_power
    }

    return d

async def main():
    devices = await BleakScanner.discover(return_adv=True)

    bt05: BLEDevice

    for device in devices:
        data = getDeviceDataFromDevice(devices[device])

        if data.get("name") == DEVICE_NAME:
            bt05 = data.get("device")
            break

    if not bt05:
        return
    
    async with BleakClient(bt05, pair=True) as client:
        print("is connected?: " + str(client.is_connected))

        while True:
            q = input("data: ")

            if q.lower() == "quit":
                break

            q += "\n\r"

            await client.write_gatt_char(CHAR_UUID, q.encode(), response=False)

    
    print("device disconnected. program quitting.")
    
asyncio.run(main())
