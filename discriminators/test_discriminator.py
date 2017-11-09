from magic_computer_comms.data_model.discriminators import Discriminators

class TestDiscriminator(Discriminators):
    def get_pertinent_signal(self, position_data, signal_data):
        return "1"
    