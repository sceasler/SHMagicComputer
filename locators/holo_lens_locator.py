"""
Provides the interface for interacting with
The Microsoft Hololens for location
"""

import json
import os
from magic_computer_comms.data_model.locators import Locators
from magic_computer_comms.io.comm_sender import ThreadedSender
from magic_computer_comms.io.comm_server import ThreadedServer

class HoloLensLocator(Locators):
    """
    Defines the interface for the HoloLens location service
    """

    def __init__(self, options):
        super(HoloLensLocator, self).__init__(options)

        if "send_host" in options:
            s_host = options["send_host"]
        else:
            s_host = None

        if "send_port" in options:
            s_port = int(options["send_port"])
        else:
            s_port = None

        r_host = options["receive_host"]
        r_port = int(options["receive_port"])

        if not (s_host is None or s_port is None):
            self.sender = ThreadedSender(s_host, s_port)

            if os.environ['magic_computer-debug'] == "true":
                print("Set up to send locator requests to UDP " + s_host + ":" + s_port)

        self.receiver = ThreadedServer(r_host, r_port, self.receive_data)

        self.received_data = {}
        self.received_data["posX"] = 0
        self.received_data["posY"] = 0
        self.received_data["posZ"] = 0
        self.received_data["rotX"] = 0
        self.received_data["rotY"] = 0
        self.received_data["rotZ"] = 0
        self.received_data["id"] = "None"

    def parse_locator(self, message: str):
        message_json = json.loads(message)

        if message_json.MessageType == "PosRotMsg":
            return message_json

        return None

    def start(self):
        """
        Starts the Locator listener
        """
        self.receiver.listen()

        if os.environ["magic_computer_debug"] == "true":
            print("locator listener started on port " + str(self.receiver.port))
