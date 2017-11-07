"""
Main entry point.  Defines services and launches app.
"""
import time
from magic_computer_comms.startup import Startup
from magic_computer_comms.io.view_request_types import RequestType

APP = Startup()

(VIEWER, ALGO, DISCRIMINATOR, RECEIVER) = APP.configure()

APP.start()

def printit():
    """
    test method
    """
    while True:
        time.sleep(1.0)
        VIEWER.send_request(RequestType.positionandrotation, '')

printit()
