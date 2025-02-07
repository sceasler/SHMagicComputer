"""
test discriminator implementation
"""

from magic_computer_comms.data_model.discriminators import Discriminators

class TestDiscriminator(Discriminators):
    """
    test discriminator implementation
    """
    def get_pertinent_signal(self, position_data, signal_data, additional_data):
        signals = self.signal_datastore.get_signal_names()

        return str(1),additional_data

        for signal in signals:
            if self.signal_datastore.get_latest_position(signal)[0]["posX"] == 0:
                return signal

        return str(len(signals) + 1)
