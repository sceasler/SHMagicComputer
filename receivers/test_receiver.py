"""
A test receiver formatter
"""
#import asyncio
import threading
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

        if not options is None:
            host = options["receiver_host"]
            port = int(options["receiver_port"])

            self.server = ThreadedServer(host, port, self.controller.process_signal_detect)
        else:
            self.server = None

    def data_push(self):
        """
        Test method to mock data from a receiver
        """

        data = "test"
        while True:
            self.controller.process_signal_detect(data)
            time.sleep(1)
            #await asyncio.sleep(1.0)

    def start(self):
        """
        Begins to listen to receive events
        """

        if not self.server is None:
            self.server.listen()

            if os.environ["magic_computer_debug"] == "true":
                print("Receiver listener started on port " + str(self.server.port))

        threading.Thread(target=self.data_push).start()
