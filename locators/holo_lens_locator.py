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

    # def __init__(self, datastore: SignalDatastore, options):
    #     super(HoloLensLocator, self).__init__(datastore, options)

    #     if not options is None:
    #         if "send_host" in options:
    #             s_host = options["send_host"]
    #         else:
    #             s_host = None

    #         if "send_port" in options:
    #             s_port = int(options["send_port"])
    #         else:
    #             s_port = None

    #         r_host = options["receive_host"]
    #         r_port = int(options["receive_port"])

    #         if not (s_host is None or s_port is None):
    #             self.sender = ThreadedSender(s_host, s_port)

    #             if os.environ['magic_computer-debug'] == "true":
    #                 print("Set up to send locator requests to UDP " + s_host + ":" + s_port)

    #         self.receiver = ThreadedServer(r_host, r_port, self.receive_data)
    #     else:
    #         self.receiver = None

    def process_message(self, message: dict):
        super(HoloLensLocator, self).process_message(message)
        self.datastore.update_sensor_position(self.__parse_json(message))

    def __parse_json(self, message_json: dict) -> dict:
        if "msgType" in message_json:
            if message_json["msgType"] == "PosRotMsg" or message_json["msgType"] == "PosUpdate":
                return message_json

        if "messageType" in message_json:
            message_json["rotX"] = 0
            message_json["rotY"] = 0
            message_json["rotZ"] = 0

            return message_json

        return None

    # def parse_locator(self, message: bytearray):
    #     #parse into string
    #     message_string = message.decode('utf_8')
    #     message_json = json.loads(message_string)

    #     return self.__parse_json(message_json)

    # def start(self):
    #     """
    #     Starts the Locator listener
    #     """
    #     if not self.receiver is None:
    #         self.receiver.listen()

    #         if os.environ["magic_computer_debug"] == "true":
    #             print("locator listener started on port " + str(self.receiver.port))
