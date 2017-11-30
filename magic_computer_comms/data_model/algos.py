"""
Superclass for all algo implementations
"""

from magic_computer_comms.datastore.signal_datastore import SignalDatastore

class Algos(object):
    """
    Algos template.  All algo implementations should inherit from this
    """
    def __init__(self, signal_datastore: SignalDatastore, options: dict):
        self.signal_datastore = signal_datastore
        self.options = options

    def refine_position(self, signal_id: str, position_data: dict) -> dict:
        """
        Executes refinement algorithm and returns updated position data

        return value is a dictionary with the following fields:
        posX,
        posY,
        posZ
        """
        pass
