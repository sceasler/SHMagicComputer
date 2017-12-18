"""
inheritable class for listening on the common listener
"""

import os

class ListenerSubscriber(object):
    """
    implementation of the listener
    """

    def process_message(self, message: dict) -> None:
        """
        Called when the common listener receives a message with the
        appropriate keyword
        """
        if os.environ["magic_computer_debug"] == "true":
            print("Received message " + message)
