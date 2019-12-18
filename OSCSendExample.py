# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
import time

# Start the system.
osc_startup()

# Make client channels to send packets.
osc_udp_client("192.168.1.208", 2000, "aclientname")

# Build a simple message and send it.
msg = oscbuildparse.OSCMessage("/test/me", ",sif", ["text1", 672, 8.871])
osc_send(msg, "aclientname")

# Build a message with autodetection of data types, and send it.
msg = oscbuildparse.OSCMessage("/test/me", None, ["text2", 672, 8])
osc_send(msg, "aclientname")

finished = False
while not finished:
    osc_process()


# Properly close the system.
osc_terminate()