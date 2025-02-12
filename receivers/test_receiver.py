"""
A test receiver formatter
"""
#import asyncio
import threading
import time
import os
import json
from magic_computer_comms.data_model.receivers import Receivers
from magic_computer_comms.io.comm_server import ThreadedServer
from magic_computer_comms.data_model.optioned_signal_data import OptionedSignalData
from magic_computer_comms.controller.controller import Controller
from magic_computer_comms.data_model.position_data import PositionData

class BasicViewerMessage(object):
    def __init__(self, id: int, msgType: str, angle: float):
        self.id = id
        self.angle = angle
        self.msgType = msgType

    def serialize(self, encoding: str) -> str:
        ret_val = self.__dict__
        
        return json.dumps(ret_val).encode(encoding)

class TestReceiver(Receivers):
    """
    Test receiver formatter
    """
    def __init__(self, controller: Controller, options):
        super(TestReceiver, self).__init__(controller, options)

        if not options is None:
            host = options["receiver_host"]
            port = int(options["receiver_port"])

            self.server = ThreadedServer(host, port, self.send_to_controller)
        else:
            self.server = None

    def send_to_controller(self, signal_data: bytearray):
        #take received data  and convert to OptionedsignalData

        ret_val = OptionedSignalData()

        self.controller.process_signal_detect(ret_val)

    def data_push(self):
        """
        Test method to mock data from a receiver
        """

        data = OptionedSignalData()
        data.signal_data = PositionData()

        mockRotX = "0"

        #someThing = BasicViewerMessage("1", "LobUpdate", )

        #with open('mock_data.txt') as data_file:
        #    someThing = BasicViewerMessage("1", "LobUpdate", data_file.read())

        data.signal_data.posX = "0"
        data.signal_data.posY = "0"
        data.signal_data.posZ = "0"
        data.signal_data.rotY = "0"
        data.signal_data.rotZ = "0"

        data.optional_data = "optioned"

        while True:
            with open('mock_data.txt') as data_file:
                data.signal_data.rotX = data_file.read()

            self.controller.process_signal_detect(data)
            time.sleep(1)
            #await asyncio.sleep(1.0)

    def start(self):
        """
        Begins to listen to receive events
        """

        if not self.server is None:
            self.server.listen()

            if os.environ["magic_computer_debug"] == "true":
                print("Receiver listener started on port " + str(self.server.port))

        threading.Thread(target=self.data_push).start()
