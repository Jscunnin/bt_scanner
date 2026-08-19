# bt_scanner
Raspberry Pi Bluetooth scanner to track devices that come in and out of range

## Logging
There are 3 different logs currently. 

devices.log logs devices that have been seen. If a device has been recognized then it will be re logged every ten minutes.

knownAddresses.log logs all addresses that have been found previously and logs the first time they were found.

lastKnown.log logs addresses that were found in the most recent scan and when they were last seen.

## Events
In order to track when specific events occur in the logs there is a tool called eventTracker.py

Run this with an argument of what event message you would like in the logs and it will put the event into the appropriate logs. 

Formatting for the event log will always be `****************EVENT****************`
