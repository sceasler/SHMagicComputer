"""
Template for all Discriminators, which
identify which signal has been detected
"""
from typing import Tuple
from magic_computer_comms.data_model.listener_subscriber import ListenerSubscriber
from magic_computer_comms.datastore.signal_datastore import SignalDatastore

class Discriminators(ListenerSubscriber):
    """
    Template discriminator.  All discriminators inherit from this
    """
    def __init__(self, signal_datastore: SignalDatastore, options: dict):
        self.signal_datastore = signal_datastore
        self.options = options

    def get_pertinent_signal(self, position_data: dict, signal_data: dict, additional_data: dict) -> Tuple[str,dict]:
        """
        ABSTRACT

        Method to determine which signal was detected

        This method must return a tuyple with a string labeling the signal name, and a dictionary of the additional data
        """
        pass
