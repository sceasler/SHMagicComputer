"""
Template for all Discriminators, which
identify which signal has been detected
"""

from magic_computer_comms.datastore.signal_datastore import SignalDatastore

class Discriminators(object):
    """
    Template discriminator.  All discriminators inherit from this
    """
    def __init__(self, signal_datastore: SignalDatastore):
        self.signal_datastore = signal_datastore

    def get_pertinent_signal(self, position_data, signal_data):
        """
        Method to determine which signal was detected
        """
        pass
