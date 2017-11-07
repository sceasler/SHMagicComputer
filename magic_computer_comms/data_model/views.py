"""
Super-type of all views
"""

from magic_computer_comms.io.view_comm_sender import ThreadedSender

class Views(object):
    """
    All views inherit from this class for their method list
    """
    def __init__(self, viewType: str, host: str, port: int):
        self.view_type = viewType
        self.sender = ThreadedSender(host, port)

    def parse_view(self, message):
        """
        Provides logic for parsing received messages
        """
        pass

    def send_request(self, request_type, parameters):
        """
        Provides logic for formatting requests
        """
        pass
