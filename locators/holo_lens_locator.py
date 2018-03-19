"""
Provides the interface for interacting with
The Microsoft Hololens for location
"""

#import json
#import os
from magic_computer_comms.data_model.locators import Locators
#from magic_computer_comms.io.comm_sender import ThreadedSender
#from magic_computer_comms.io.comm_server import ThreadedServer
#from magic_computer_comms.datastore.signal_datastore import SignalDatastore

class HoloLensLocator(Locators):
    """
    Defines the interface for the HoloLens location service
    """

    def process_message(self, message: dict):
        super(HoloLensLocator, self).process_message(message)
        self.datastore.update_sensor_position(self.__parse_json(message))

    def __parse_json(self, message_json: dict):
        if "msgType" in message_json:
            if message_json["msgType"] == "PosRotMsg" or message_json["msgType"] == "PosUpdate":
                return message_json

        if "messageType" in message_json:
            message_json["rotX"] = 0
            message_json["rotY"] = 0
            message_json["rotZ"] = 0

            return message_json

        return None
