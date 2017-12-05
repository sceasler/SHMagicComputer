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

    def parse_locator(self, message) -> dict:
        """
        Provides logic for parsing received messages

        Output must be a dictionary with the following fields:
        (need to define the position/rotation values as well)
        posX: X position
        posY: Y position
        posZ: Z position
        rotX: X rotation
        rotY: Y rotation
        rotZ: Z rotation
        id: The id of the locator

        """
        pass

    def send_request(self, request_type: RequestType, parameters) -> None:
        """
        Provides logic for formatting requests

        This is used if the data is not pushed to the server,
        and the server needs to request the data
        """
        pass

    def receive_data(self, message) -> None:
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
            loc_id = self.received_data["id"]

            message = "locator " + str(loc_id) + " sent location " + str(pos_x) + ", " + str(pos_y) + ", " + str(pos_z)
            message += ", " + str(rot_x) + ", " + str(rot_y) + ", " + str(rot_z)

            print(message)

    async def refresh_position_data(self) -> dict:
        """
        Sends a request for updated location information, and awaits a response
        """
        self.waiting_on_data = True
        self.send_request(RequestType.positionandrotation, '')

        while self.waiting_on_data:
            await asyncio.sleep(.005)

        return self.get_position_data()

    def get_position_data(self) -> dict:
        """
        Returns the last reported position
        """
        if self.received_data is not None:
            return self.received_data

    def start(self) -> None:
        """
        Starts the Locator listener
        """
        pass
