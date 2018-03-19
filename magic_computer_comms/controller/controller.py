"""
Defines the Controller
"""
#import asyncio
import os
from typing import List
from magic_computer_comms.data_model.algos import Algos
from magic_computer_comms.data_model.discriminators import Discriminators
from magic_computer_comms.data_model.views import Views
from magic_computer_comms.datastore.signal_datastore import SignalDatastore
from magic_computer_comms.data_model.optioned_signal_data import OptionedSignalData

class Controller(object):
    """
    Controls all the signal processing received from the receiver
    """
    def __init__(self, datastore: SignalDatastore, discriminator: Discriminators, algo: Algos, viewers: List[Views]):
        self.datastore: SignalDatastore = datastore
        self.discriminator: Discriminators = discriminator
        self.algo: Algos = algo
        self.viewers: List[Views] = viewers

    async def __process_command(self, command_data) -> None:
        pass

    """
    This is invoked by the receiver
    """
    def __process_signal_detect__(self, receiver_data: OptionedSignalData) -> None:
        position_data = self.datastore.get_sensor_position()

        signal_data = receiver_data.signal_data
        additional_data = receiver_data.optional_data

        if not bool(position_data):
            return

        pertinent_signal, additional_data = self.discriminator.get_pertinent_signal(position_data, signal_data, additional_data)

        if pertinent_signal is None:
            return

        refined_position, additional_data = self.algo.refine_position(pertinent_signal, position_data, additional_data)

        if refined_position is None:
            return

        for viewer in self.viewers:
            viewer.update_view(pertinent_signal, refined_position, additional_data)

    def process_command(self, command_data):
        """
        Called when the user issues a command
        """

        self.__process_signal_detect__(command_data)

        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(self.__process_signal_detect__(command_data))

    def process_signal_detect(self, signal_data: OptionedSignalData):
        """
        Called by the receiver when new signal data is available
        """

        self.__process_signal_detect__(signal_data)

        if os.environ["magic_computer_debug"] == "true":
            print("Controller processing complete")

        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(self.__process_signal_detect__(signal_data))
