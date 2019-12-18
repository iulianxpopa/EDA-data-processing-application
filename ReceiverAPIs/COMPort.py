import sys
import serial
import serial.tools.list_ports

class COMPort():
    """ Select the proper FMCI COM Port in order to receive
    data through it.
    """

    def __init__(self):
        self.port = self.__find_port()

    def __find_port(self):
        """ Try to automatically select the FMCI serial port if it's 
        the single one connected. If there are more, the user needs to
        select the right one from a list by by inputting it's index. 
        """
        if '-i' in sys.argv[1:]: # Get input COM
            port_idx = sys.argv.index('-i') + 1
            port = sys.argv[port_idx]
        else: # Search an USB port
            ports_COM = []

            for port_no, description, _ in list(serial.tools.list_ports.comports()):
                if 'USB' in description:
                    ports_COM.append(port_no)
            
            if len(ports_COM) > 1:  # If more than 1 USBs are connected to the computer
                print('Selection oF FMCI serial port (Select one)')
                for i in range(len(ports_COM)):
                    print('Available Ports: ' + str(i) + '\n')
                print('Selected USB: ')
                try:
                    user_input = int(input())
                except:
                    print('Please type one of the options')
                port = ports_COM[user_input]
            else:  # If only one USB port is connected
                port = ports_COM[0]
        return port
