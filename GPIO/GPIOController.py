import RPi.GPIO as GPIO

def StartSession():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

def StopSession():
    GPIO.cleanup()