import RPi.GPIO as GPIO
import time
import queue
import threading

class Led:
    def __init__(self, idNo):
        self.idNo = idNo
        self._communicationQueue = None
        self._blinkThread = None
        GPIO.setup(self.idNo, GPIO.OUT)
    
    def On(self):
        GPIO.output(self.idNo, GPIO.HIGH)
    
    def Off(self):
        GPIO.output(self.idNo, GPIO.LOW)
    
    def Blink(self, blinkDelay, queue):
        while True:
            self.On()
            time.sleep(blinkDelay)
            self.Off()
            time.sleep(blinkDelay)
            
            if not queue.empty():
                cmd = queue.get()
                if isinstance(cmd, str) and cmd == 'quit':
                    break
    
    def StartBlinking(self, blinkDelay):
        if self._blinkThread is None:
            self._communicationQueue = queue.Queue()
            self._blinkThread = threading.Thread(target=self.Blink, args=[blinkDelay, self._communicationQueue])
            self._blinkThread.start()

    def StopBlinking(self):
        self._communicationQueue.put('quit')
        self._blinkThread.join()
        self._communicationQueue = None
        self._blinkThread = None
