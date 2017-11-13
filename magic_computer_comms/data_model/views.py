"""
Super-type of all views
"""

from magic_computer_comms.io.comm_sender import ThreadedSender

class Views(object):
    """
    All views inherit from this class for their method list
    """
    def __init__(self, options):
        host = options["view_host"]
        port = int(options["view_port"])

        self.sender = ThreadedSender(host, port)
        self.options = options

    def update_view(self, pertinent_signal, refined_position):
        """
        Provides logic for formatting requests
        """
        pass
