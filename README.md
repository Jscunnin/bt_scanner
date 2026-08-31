# BT Scanner

A Raspberry Pi–based Bluetooth scanner that tracks when known devices come in and out of range.

## Why I built it

I wanted to be able to detect when I arrived to my home in order to trigger certain events such as lighting or music. As well as this I wanted to be able to detect when friends were in range to change the houses enviornment and atmosphere. AKA 
play different music, make lights brighter, etc.

## How it works

- Runs on a Raspberry Pi with Bluetooth scanning capability
- Periodically scans for nearby Bluetooth devices
- Compares detected device addresses against a list of known/tracked devices
- Logs important events via a web api. a very simple web API has been implemented for this feature. 

## Hardware / Requirements

- Raspberry Pi (or any Linux device with Bluetooth)
- Bleak


## Notes

This started as a personal presence-detection experiment. There are many limitations to this program. Devices must be on and in pairing mode to be seen and range is limited by the pi's hardware.
