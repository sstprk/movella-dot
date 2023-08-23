import asyncio 
from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
import logging

logging.basicConfig(filename = 'app.log', level = logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    try:
        logger.info("Scanning..")
        devices = await BleakScanner.discover()
        logger.info("%d devices found", len(devices))
        logger.info("Printing devices..")
        for dev in devices:
            print(dev)
        try:
            address = "D4:22:CD:00:03:9B"
            logging.info("Starting process")
            async with BleakClient(address) as client:
                logger.info("Getting client services..")
                svcs = await client.read_gatt_char("15170x0886-4947-11E9-8646-D663BD873D93")
                logger.info("Got %d services", len(svcs))
                logger.info("Printing services..")
            print("Services:")
            for service in svcs:
                print(service)
        except:
            logger.exception("Can't start this section")
    except:
        logger.exception("Func has a problem")

asyncio.run(main())

#D4:22:CD:00:03:9B: Xsens DOT
#D4:22:CD:00:03:78: Xsens DOT
#D4:22:CD:00:03:83: Xsens DOT
#Company = 15170x0886-4947-11E9-8646-D663BD873D93
#Configuration service = 15170x1000-4947-11E9-8646-D663BD873D93
#Measurement Service = 15170x2000-4947-11E9-8646-D663BD873D93

