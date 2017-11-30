"""
Template for all Discriminators, which
identify which signal has been detected
"""

from magic_computer_comms.datastore.signal_datastore import SignalDatastore

class Discriminators(object):
    """
    Template discriminator.  All discriminators inherit from this
    """
    def __init__(self, signal_datastore: SignalDatastore, options: dict):
        self.signal_datastore = signal_datastore
        self.options = options

    def get_pertinent_signal(self, position_data: dict, signal_data: dict) -> str:
        """
        Method to determine which signal was detected

        This method must return a string labeling the signal name
        """
        pass
