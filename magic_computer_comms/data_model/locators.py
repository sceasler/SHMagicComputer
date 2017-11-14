"""
Super-type of all locators
"""
import asyncio
import os
from magic_computer_comms.io.locator_request_types import RequestType
class Locators(object):
    """
    All locators inherit from this class for their method list
    """

    def __init__(self, options):
        self.received_data = None
        self.waiting_on_data = False
        self.options = options

    def parse_locator(self, message):
        """
        Provides logic for parsing received messages

        The parser should present the data in a dictionary:

        {posX, posY, posZ, rotX, rotY, rotZ}
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
            pos_x = self.received_data["posX"]
            pos_y = self.received_data["posY"]
            pos_z = self.received_data["posZ"]
            rot_x = self.received_data["rotX"]
            rot_y = self.received_data["rotY"]
            rot_z = self.received_data["rotZ"]

            print("viewer sent position data " + pos_x + ", " + pos_y + ", " + pos_z)
            print("viewer sent rotation data " + rot_x + ", " + rot_y + ", " + rot_z)

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
        pass
