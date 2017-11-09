"""
Template for all receiver formatters
"""

from magic_computer_comms.controller.controller import Controller
from magic_computer_comms.io.comm_server import ThreadedServer

class Receivers(object):
    """
    All receiver formatters inherit from here.  This will
    convert data from a receiver into a common format and
    notify the controller of a detect event
    """
    def __init__(self, controller: Controller, host, port):
        self.controller = controller
        self.server = ThreadedServer(host, port, self.controller.process_signal_detect)

    def start(self):
        """
        Begins to listen to receive events
        """
        self.server.listen_to_client()


