"""
Super-type of all locators
"""
#import asyncio
import os
from magic_computer_comms.data_model.listener_subscriber import ListenerSubscriber
#from magic_computer_comms.io.locator_request_types import RequestType
from magic_computer_comms.datastore.signal_datastore import SignalDatastore
class Locators(ListenerSubscriber):
    """
    All locators inherit from this class for their method list
    """

    def __init__(self, datastore: SignalDatastore, options: dict):
        self.received_data = None
        self.waiting_on_data = False
        self.options = options
        self.datastore = datastore

    # def parse_locator(self, message) -> dict:
    #     """
    #     Provides logic for parsing received messages

    #     Output must be a dictionary with the following fields:
    #     posX: X position
    #     posY: Y position
    #     posZ: Z position
    #     rotX: X rotation
    #     rotY: Y rotation
    #     rotZ: Z rotation
    #     id: The id of the locator

    #     If only partial information is to be provided, do not
    #     include the empty fields in the dictionary

    #     """
    #     pass

    # def send_request(self, request_type: RequestType, parameters) -> None:
    #     """
    #     Provides logic for formatting requests

    #     This is used if the data is not pushed to the server,
    #     and the server needs to request the data
    #     """
    #     pass

    def __debug_receive(self, message: dict):
        if os.environ["magic_computer_debug"] == "true":
            debug_data = self.get_position_data()
            pos_x = debug_data["posX"]
            pos_y = debug_data["posY"]
            pos_z = debug_data["posZ"]
            rot_x = debug_data["rotX"]
            rot_y = debug_data["rotY"]
            rot_z = debug_data["rotZ"]
            loc_id = debug_data["id"]

            message = "locator " + str(loc_id) + " sent location " + str(pos_x) + ", " + str(pos_y) + ", " + str(pos_z)
            message += ", " + str(rot_x) + ", " + str(rot_y) + ", " + str(rot_z)

            print(message)

    def process_message(self, message: dict):
        self.__debug_receive(message)

    # def receive_data(self, message) -> None:
    #     """
    #     Method called when the server receives data from the locator
    #     not used when utilizing the common listener
    #     """
    #     self.datastore.update_sensor_position(self.parse_locator(message))
    #     self.waiting_on_data = False

    #     self.__debug_receive(message)

    # async def refresh_position_data(self) -> dict:
    #     """
    #     Sends a request for updated location information, and awaits a response
    #     """
    #     self.waiting_on_data = True
    #     self.send_request(RequestType.positionandrotation, '')

    #     while self.waiting_on_data:
    #         await asyncio.sleep(.005)

    #     return self.get_position_data()

    def get_position_data(self) -> dict:
        """
        Returns the last reported position
        """
        self.received_data = self.datastore.get_sensor_position()

        if self.received_data is not None:
            return self.received_data

    def start(self) -> None:
        """
        Starts the Locator listener
        """
        pass
