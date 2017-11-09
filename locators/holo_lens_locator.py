"""
Provides the interface for interacting with
The Microsoft Hololens for location
"""

import json
from magic_computer_comms.data_model.locators import Locators

class HoloLensLocator(Locators):
    """
    Defines the interface for the HoloLens location service
    """

    def __init__(self, r_host: str, r_port: int, s_host: str, s_port: int):
        super(HoloLensLocator, self).__init__(r_host=r_host, r_port=r_port, s_host=s_host, s_port=s_port)

    def parse_locator(self, message: str):
        message_json = json.loads(message)

        if message_json.MessageType == "PosRotMsg":
            return message_json

        return None
