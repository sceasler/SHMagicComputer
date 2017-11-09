"""
Super-type of all views
"""

from magic_computer_comms.io.comm_sender import ThreadedSender

class Views(object):
    """
    All views inherit from this class for their method list
    """
    def __init__(self, host: str, port: int):
        self.sender = ThreadedSender(host, port)

    def update_view(self, pertinent_signal, refined_position):
        """
        Provides logic for formatting requests
        """
        pass
