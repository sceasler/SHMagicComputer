"""
Superclass for all algo implementations
"""

from magic_computer_comms.datastore.signal_datastore import SignalDatastore

class Algos(object):
    """
    Algos template.  All algo implementations should inherit from this
    """
    def __init__(self, signal_datastore: SignalDatastore):
        self.signal_datastore = signal_datastore

    def refine_position(self, signal_id, position_data):
        """
        Executes refinement algorithm and returns updated position data
        """
        pass
