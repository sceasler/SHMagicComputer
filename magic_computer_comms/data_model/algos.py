from magic_computer_comms.datastore.signal_datastore import SignalDatastore

class Algos(object):
    def __init__(self, signal_datastore: SignalDatastore):
        self.signal_datastore = signal_datastore

    def refine_position(self, signal_id, position_data):
        pass
