"""
Super-type of all locators
"""
import asyncio
import os
from magic_computer_comms.io.comm_sender import ThreadedSender
from magic_computer_comms.io.comm_server import ThreadedServer
from magic_computer_comms.io.locator_request_types import RequestType

class Locators(object):
    """
    All locators inherit from this class for their method list
    """

    def __init__(self, options):

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

        self.received_data = None
        self.waiting_on_data = False
        self.receiver = ThreadedServer(r_host, r_port, self.receive_data)

    def parse_locator(self, message):
        """
        Provides logic for parsing received messages
        """

    def send_request(self, request_type, parameters):
        """
        Provides logic for formatting requests
        """
        pass

    def receive_data(self, message):
        """
        Method called when the server receives data from the locator
        """
        self.received_data = self.parse_locator(message)
        self.waiting_on_data = False

        if os.environ["magic_computer_debug"] == "true":
            x_pos = self.received_data["posX"]
            y_pos = self.received_data["posY"]
            z_pos = self.received_data["posZ"]
            x_rot = self.received_data["rotX"]
            y_rot = self.received_data["rotY"]
            z_rot = self.received_data["rotZ"]

            print("viewer sent position data " + x_pos + ", " + y_pos + ", " + z_pos)
            print("viewer sent rotation data " + x_rot + ", " + y_rot + ", " + z_rot)

    async def refresh_position_data(self):
        """
        Sends a request for updated location information, and awaits a response
        """
        self.waiting_on_data = True
        self.send_request(RequestType.positionandrotation, '')

        while self.waiting_on_data:
            await asyncio.sleep(.005)

        return self.get_position_data()

    def get_position_data(self):
        """
        Returns the last reported position
        """
        if self.received_data is not None:
            return self.received_data

    def start(self):
        """
        Starts the Locator listener
        """
        self.receiver.listen()

        if os.environ["magic_computer_debug"] == "true":
            print("locator listener started on port " + str(self.receiver.port))
