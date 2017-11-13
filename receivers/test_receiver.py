"""
A test receiver formatter
"""

import time
import os
from magic_computer_comms.data_model.receivers import Receivers
from magic_computer_comms.io.comm_server import ThreadedServer

class TestReceiver(Receivers):
    """
    Test receiver formatter
    """
    def __init__(self, controller, options):
        super(TestReceiver, self).__init__(controller, options)
        host = options["receiver_host"]
        port = int(options["receiver_port"])

        self.server = ThreadedServer(host, port, self.controller.process_signal_detect)

    def data_push(self):
        """
        Test method to mock data from a receiver
        """

        data = "test"
        while True:
            self.controller.process_signal_detect(data)
            time.sleep(2)
            #await asyncio.sleep(2)

    def start(self):
        """
        Begins to listen to receive events
        """
        self.server.listen()

        if os.environ["magic_computer_debug"] == "true":
            print("Receiver listener started on port " + str(self.server.port))
