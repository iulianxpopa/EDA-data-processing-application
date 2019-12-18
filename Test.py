import threading
import time
import GPIO.GPIOController
from GPIO.Led import Led
import queue
from ReceiverAPIs.BluetoothDataReceiver import BluetoothDataReceiver
from Configuration.BluetoothReceiverConfiguration import BluetoothReceiverConfiguration
from bitalino import BITalino

GPIO.GPIOController.StartSession()

#define leds to be used
redLed = Led(17)
greenLed = Led(18)

#load configuration from json
config = BluetoothReceiverConfiguration()
config.LoadConfiguration()

#data buffer used to transfer data between receiving, processing and delivery threads
dataBuffer = queue.Queue()

#blinking red signls receiving signal hasn't started yet
redLed.StartBlinking(0.1)

#initialise receiver
receiver = BluetoothDataReceiver(dataBuffer, config)

#start data aquisition
receiver.Start()
redLed.StopBlinking()

#green signals that trasfer is working
greenLed.On()

#wait for a while
time.sleep(10)

#stop data aquisition
receiver.Stop()
greenLed.Off()