import asyncio
from bleak import BleakScanner
import os
from datetime import datetime
import time

addresses = []

limit = 600 #time difference in seconds needed to relog a device that was previously discovered

#Variable to store whenan address was last seen
lastSeen = {}

dataFolder = os.path.join(os.getcwd(), 'data')
deviceFile = os.path.join(os.getcwd(), 'data', 'devices.log')
addressesFile = os.path.join(dataFolder, 'knownAddresses.log')
lastSeenFile = os.path.join(dataFolder, 'lastSeen.log')

def init():
	global addresses, lastSeen

	if not os.path.exists(dataFolder):
		os.mkdir(dataFolder)
		with open(deviceFile, 'w') as file:
			file.write("TIME,NAME,ADDRESS,RSSI/SIGNAL\n") #Writing headers for device file

		with open(addressesFile, 'w') as file:
			file.write("ADDRESS,FIRST_SEEN\n") #Writing headers for address file

	#LOADING PREVIOUS DATA INTO VARS:
	with open(addressesFile, 'r') as file:
		firstLine = True;
		for line in file:
			if not firstLine and ',' in line:
				addresses.append(line.split(',')[0])
				print(f"Device added: {line.split(',')[0]}")
			else:
				firstLine = False
	if os.path.isfile(lastSeenFile):
		with open(lastSeenFile, 'r') as file:
			firstLine = True;
			for line in file:
				address = line.split(',')[0]
				time = line.split(',')[1]
				lastSeen[address] = datetime.fromisoformat(time.rstrip())

def handleNewDevice(device, data):
        global addresses, lastSeen
        with open(deviceFile, 'a') as file:
                file.write(f"{datetime.now()},{device.name},{device.address},{data.rssi}\n")
        print(f"NEW DEVICE: {datetime.now()},{device.name},{device.address},{data.rssi}\n")
        addresses.append(device.address)
        lastSeen[device.address] = datetime.now()

        with open(addressesFile, 'a') as file:
                file.write(f"{device.address},{datetime.now()}\n")

def handleOldDevice(device, data):
	if (datetime.now() - lastSeen[device.address]).total_seconds() > limit:
		lastSeen[device.address] = datetime.now()
		print(f"OLD DEVICE REFOUND: {datetime.now()},{device.name},{device.address},{data.rssi}\n")
		with open(deviceFile, 'a') as file:
			file.write(f"{datetime.now()},{device.name},{device.address},{data.rssi}\n")

def callback(device, data):
	global addresses, lastSeen

	#Handle new devices when discovered
	if device.address not in addresses:
		handleNewDevice(device, data)

	#Handle old devices
	elif device.address in lastSeen.keys():
		handleOldDevice(device, data)
	#Logging all address captured recently and when they were last seen
	with open(lastSeenFile, 'w') as file:
		for address in lastSeen.keys():
			file.write(f"{address},{lastSeen[address]}\n")

async def main():
	scanner = BleakScanner(detection_callback=callback)
	await scanner.start()
	await asyncio.sleep(5.0)
	await scanner.stop()

init()
while True:
	asyncio.run(main())
	time.sleep(10)
