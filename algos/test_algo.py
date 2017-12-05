"""
Test algo implemenation
"""
from magic_computer_comms.data_model.algos import Algos

class TestAlgo(Algos):
    """
    test algo implementation
    """
    def refine_position(self, signal_id, position_data):
        calculated_position = {"posX": position_data["posX"], "posY": position_data["posY"], "posZ": position_data["posZ"]}

        self.signal_datastore.update_position(signal_id, position_data, calculated_position)

        return calculated_position
