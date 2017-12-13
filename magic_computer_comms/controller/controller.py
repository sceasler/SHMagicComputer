"""
Defines the Controller
"""
import asyncio
from magic_computer_comms.data_model.algos import Algos
from magic_computer_comms.data_model.discriminators import Discriminators
from magic_computer_comms.data_model.views import Views
from magic_computer_comms.data_model.locators import Locators

class Controller(object):
    """
    Controls all the signal processing received from the receiver
    """
    def __init__(self, locator, discriminator, algo, viewer):
        self.locator: Locators = locator
        self.discriminator: Discriminators = discriminator
        self.algo: Algos = algo
        self.viewer: Views = viewer

    def start(self):
        """
        Starts all signal processing services
        """
        self.locator.start()

    async def __process_signal_detect__(self, signal_data):
        position_data = self.locator.get_position_data()
        pertinent_signal = self.discriminator.get_pertinent_signal(position_data, signal_data)
        refined_position = self.algo.refine_position(pertinent_signal, position_data)
        self.viewer.update_view(pertinent_signal, refined_position)

    def process_signal_detect(self, signal_data):
        """
        Called by the receiver when new signal data is available
        """

        loop = asyncio.get_event_loop()

        loop.run_until_complete(self.__process_signal_detect__(signal_data))
