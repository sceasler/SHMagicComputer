"""
Superclass for all algo implementations
"""
from typing import Tuple
from magic_computer_comms.data_model.listener_subscriber import ListenerSubscriber
from magic_computer_comms.datastore.signal_datastore import SignalDatastore
from magic_computer_comms.data_model.position_data import PositionData

class Algos(ListenerSubscriber):
    """
    Algos template.  All algo implementations should inherit from this
    """
    def __init__(self, signal_datastore: SignalDatastore, options: dict):
        self.signal_datastore = signal_datastore
        self.options = options

    def refine_position(self, signal_id: str, position_data: dict, additional_data: dict) -> Tuple[PositionData, dict]:
        """
        ABSTRACT

        Executes refinement algorithm and returns updated position data

        return value is a tuple with a PositionData and the additional data
        """
        pass
