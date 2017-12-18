"""
Defines the Controller
"""
#import asyncio
from typing import List
from magic_computer_comms.data_model.algos import Algos
from magic_computer_comms.data_model.discriminators import Discriminators
from magic_computer_comms.data_model.views import Views
from magic_computer_comms.datastore.signal_datastore import SignalDatastore

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

    def __process_signal_detect__(self, signal_data) -> None:
        position_data = self.datastore.get_sensor_position()

        if not bool(position_data):
            return

        pertinent_signal = self.discriminator.get_pertinent_signal(position_data, signal_data)

        if pertinent_signal is None:
            return

        refined_position = self.algo.refine_position(pertinent_signal, position_data)

        if refined_position is None:
            return

        for viewer in self.viewers:
            viewer.update_view(pertinent_signal, refined_position)

    def process_command(self, command_data):
        """
        Called when the user issues a command
        """

        self.__process_signal_detect__(command_data)

        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(self.__process_signal_detect__(command_data))

    def process_signal_detect(self, signal_data):
        """
        Called by the receiver when new signal data is available
        """

        self.__process_signal_detect__(signal_data)

        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(self.__process_signal_detect__(signal_data))
