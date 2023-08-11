import asyncio 
from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

async def main():
    devices =await BleakScanner.discover()
    for dev in devices:
        print(dev)

    address = "D4:22:CD:00:03:9B"
    async with BleakClient(address_or_ble_device=address, ) as client:
        svcs = await client.read_gatt_char("15170x0886-4947-11E9-8646-D663BD873D93")
    print("Services:")
    print(svcs)

if __name__ == "__main__":
    asyncio.run(main())


#D4:22:CD:00:03:9B: Xsens DOT
#D4:22:CD:00:03:78: Xsens DOT
#D4:22:CD:00:03:83: Xsens DOT
#Company = 15170x0886-4947-11E9-8646-D663BD873D93
#Configuration service = 15170x1000-4947-11E9-8646-D663BD873D93
#Measurement Service = 15170x2000-4947-11E9-8646-D663BD873D93
#Battery service = 15170x3000-4947-11E9-8646-D663BD873D93
#DFU service = 15170x4000-4947-11E9-8646-D663BD873D93
#Message service = 15170x7000-4947-11E9-8646-D663BD873D93
#Sensor basic info = 15170x1001-4947-11E9-8646-D663BD873D93
