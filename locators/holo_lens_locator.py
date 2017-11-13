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

    def __init__(self, options):
        super(HoloLensLocator, self).__init__(options)

    def parse_locator(self, message: str):
        message_json = json.loads(message)

        if message_json.MessageType == "PosRotMsg":
            return message_json

        return None
