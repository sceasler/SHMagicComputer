"""
Super-type of all locators
"""
import asyncio
from magic_computer_comms.io.comm_sender import ThreadedSender
from magic_computer_comms.io.comm_server import ThreadedServer
from magic_computer_comms.io.locator_request_types import RequestType

class Locators(object):
    """
    All locators inherit from this class for their method list
    """

    def __init__(self, r_host: str, r_port: int, s_host: str, s_port: int):

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
        if self.received_data is None:
            return (0, 0, 0, 0, 0)
        else:
            return self.received_data

    def start(self):
        """
        Starts the Locator listener
        """
        self.receiver.listen()
