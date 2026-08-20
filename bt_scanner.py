import asyncio
from bleak import BleakScanner
import os
from datetime import datetime
import time
import subprocess

addresses = []

limit = 600 #time difference in seconds needed to relog a device that was previously discovered

#Variable to store whenan address was last seen
lastSeen = {}

dataFolder = os.path.join(os.getcwd(), 'data')
deviceFile = os.path.join(os.getcwd(), 'data', 'devices.log')
addressesFile = os.path.join(dataFolder, 'knownAddresses.log')
lastSeenFile = os.path.join(dataFolder, 'lastSeen.log')
oldLogFolder = os.path.join(dataFolder, 'oldLogs/')
apiFolder = os.path.join(os.getcwd(), 'publicAPI/')
pythonBin = os.path.join(os.getcwd(), 'venv', 'bin', 'python3')
apiApp = os.path.join(apiFolder, 'main.py')

def runAPI():
	try:
		subprocess.Popen([pythonBin, apiApp], cwd=apiFolder)
	except:
		pass


def init():
	global addresses, lastSeen
	runAPI()
	if not os.path.exists(dataFolder):
		os.mkdir(dataFolder)
		os.mkdir(oldLogFolder)
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
                file.write(f"{device.address},{device.name},{datetime.now()}\n")

def handleOldDevice(device, data):
	if (datetime.now() - lastSeen[device.address]).total_seconds() > limit:
		lastSeen[device.address] = datetime.now()
		print(f"OLD DEVICE REFOUND: {datetime.now()},{device.name},{device.address},{data.rssi}\n")
		with open(deviceFile, 'a') as file:
			file.write(f"{datetime.now()},{device.name},{device.address},{data.rssi}\n")

def checkLogSize():
	'''Function to handle when the log is getting too large. This will read the size of the log 
	and if the log is too large it will only write the most recent logs to a new file.'''
	with open(deviceFile, 'r') as file:
		count = 0
		refactor = False
		for line in file:
			if count > 1000:
				refactor = True
		count += 1
		if refactor:
			newFileLocation = os.path.join(dataFolder, oldLogFolder, datetime.now().strftime("%Y-%m-%d"))
			os.rename(deviceFile, newFileLocation)
			with open(deviceFile, 'w') as file:
				file.write("TIME,NAME,ADDRESS,RSSI/SIGNAL\n")
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
cycles = 0
while True:
	runAPI()
	asyncio.run(main())
	time.sleep(10)
	if cycles > 60:
		check_log_size()

