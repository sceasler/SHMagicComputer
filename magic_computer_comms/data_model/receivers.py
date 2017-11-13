"""
Template for all receiver formatters
"""
import os
from magic_computer_comms.controller.controller import Controller
from magic_computer_comms.io.comm_server import ThreadedServer

class Receivers(object):
    """
    All receiver formatters inherit from here.  This will
    convert data from a receiver into a common format and
    notify the controller of a detect event
    """
    def __init__(self, controller: Controller, options):
        host = options["receiver_host"]
        port = int(options["receiver_port"])

        self.controller = controller
        self.server = ThreadedServer(host, port, self.controller.process_signal_detect)

    def start(self):
        """
        Begins to listen to receive events
        """
        self.server.listen()

        if os.environ["magic_computer_debug"] == "true":
            print("Receiver listener started on port " + str(self.server.port))
