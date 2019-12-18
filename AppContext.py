#Global variables
import queue
import signal

message_queue = queue.Queue()
samples_counter = {}

def __KeyboardInterrupt_handler(sig, frame):
    """ Sends everywhere the 'quit' message 
        through the global queue in order
        to close the program safely. 
    """
    message_queue.put('quit')
    print('\n')

signal.signal(signal.SIGINT, __KeyboardInterrupt_handler)
#Catches the KeyboardInterrupt(CTRL - C) 
#and call KeyboardInterrupt_handler method.
