"""
Implementation of the viewer for Microsoft HoloLens
"""

import json
import os
from magic_computer_comms.data_model.views import Views
from magic_computer_comms.io.comm_sender import ThreadedSender
from magic_computer_comms.data_model.position_data import PositionData

class ViewerMessage(object):
    def __init__(self, id: str, msgType: str, position: PositionData, additional_data: dict):
        self.id = id
        self.msgType = msgType
        self.position = position
        self.additional_data = additional_data

    def serialize(self, encoding: str) -> str:
        ret_val = self.__dict__
        ret_val["position"] = self.position.__dict__

        return json.dumps(ret_val).encode(encoding)

class BasicViewerMessage(object):
    def __init__(self, id: int, msgType: str, angle: float):#, optional_data: dict):
        self.id = id
        self.angle = angle
        self.msgType = msgType
        #self.optional_data = optional_data

    def serialize(self, encoding: str) -> str:
        ret_val = self.__dict__
        
        return json.dumps(ret_val).encode(encoding)

class HoloLensView(Views):
    """
    Provides formatting data for sending data to the HoloLens
    """
    def __init__(self, options):
        super(HoloLensView, self).__init__(options)

        host = options["view_host"]
        port = int(options["view_port"])

        self.sender = ThreadedSender(host, port)

        if os.environ['magic_computer_debug'] == "true":
            print("set up to use view at " + host + ":" + str(port) + " using UDP")

    def update_view(self, pertinent_signal, refined_position: PositionData, additional_data):
        super(HoloLensView, self).update_view(pertinent_signal, refined_position, additional_data)

        refined_position["id"] = pertinent_signal #["messageType"]
        refined_position["msgType"] = "LobUpdate" #"PosUpdate"

        #message = ViewerMessage(int(pertinent_signal), "PosUpdate", refined_position, additional_data)
        #message = BasicViewerMessage(int(pertinent_signal), "LobUpdate", float(refined_position.rotX), additional_data)
        message = BasicViewerMessage(int(pertinent_signal), "LobUpdate", float(refined_position.rotX))

        serializedMessage = message.serialize('utf-8')

        self.sender.send_to_client(serializedMessage)
