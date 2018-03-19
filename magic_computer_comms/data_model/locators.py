"""
Super-type of all locators
"""
#import asyncio
import os
from magic_computer_comms.data_model.listener_subscriber import ListenerSubscriber
#from magic_computer_comms.io.locator_request_types import RequestType
from magic_computer_comms.datastore.signal_datastore import SignalDatastore
from magic_computer_comms.data_model.position_data import PositionData
class Locators(ListenerSubscriber):
    """
    All locators inherit from this class for their method list
    """

    def __init__(self, datastore: SignalDatastore, options: dict):
        self.received_data = None
        self.waiting_on_data = False
        self.options = options
        self.datastore = datastore

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

    def get_position_data(self) -> PositionData:
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
