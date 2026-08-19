import os
import sys
from datetime import datetime

dash_amount = 20

dataFolder = os.path.join(os.getcwd(), 'data')
deviceFile = os.path.join(os.getcwd(), 'data', 'devices.log')
addressesFile = os.path.join(dataFolder, 'knownAddresses.log')
lastSeenFile = os.path.join(dataFolder, 'lastSeen.log')

if len(sys.argv) > 1:
	message = sys.argv[1]
	with open(deviceFile, 'a') as file:
		file.write(f"{'-' * dash_amount}{message}{'-' * dash_amount}\n")
	with open(addressesFile, 'a') as file:
		file.write(f"{'-' * dash_amount}{message}{'-' * dash_amount}\n")
else:
	print("must be given an arugment to work")
