"""
A test receiver formatter
"""

import json
import time
#import asyncio
from magic_computer_comms.data_model.receivers import Receivers

class TestReceiver(Receivers):
    """
    Test receiver formatter
    """
    #def __init__(self, controller, host, port):
    #    super(TestReceiver, self).__init__(controller, host, port)

    def data_push(self):
        """
        Test method to mock data from a receiver
        """
        #data = json.load("{\"type\"=\"wifi\",\"snr\"=\"0.3444\",\"channel\"=2,\"ssid\"=\"something\"}")
        data = "test"
        while True:
            self.controller.process_signal_detect(data)
            time.sleep(2)
            #await asyncio.sleep(2)

    def start(self):
        self.server.listen()
        self.data_push()
