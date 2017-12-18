"""
Multi-purpose listener available for modules
"""
import json
import os
from typing import Dict
from typing import Callable
from magic_computer_comms.io.comm_server import ThreadedServer

class Listener(object):
    """
    Sets up listener for modules to use if desired
    """
    def __init__(self, port: int, keywords: Dict[str, Callable[[str], None]]):
        self.listener = ThreadedServer("0.0.0.0", port, self.process_input)
        self.keywords = keywords

    def process_input(self, message: bytearray):
        """
        Processes received messages
        """
        message_json: dict = json.loads(message.decode('utf_8'))

        message_type = message_json["msgType"]

        if message_type in self.keywords.keys():
            klass = self.keywords[message_type]
            klass(message_json)

    def start(self):
        """
        Starts server
        """
        self.listener.listen()

        if os.environ["magic_computer_debug"] == "true":
            print("Starting Listener on port " + str(self.listener.port) + " with the following keywords:")
            for keyword in self.keywords:
                print("\t" + keyword)
