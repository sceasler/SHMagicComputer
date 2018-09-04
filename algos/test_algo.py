"""
Test algo implemenation
"""
from magic_computer_comms.data_model.algos import Algos
from magic_computer_comms.data_model.position_data import PositionData

class TestAlgo(Algos):
    """
    test algo implementation
    """
    def refine_position(self, signal_id, position_data: PositionData, signal_data: PositionData, additional_data):
        calculated_position = PositionData()
        calculated_position.posX = position_data["posX"]
        calculated_position.posY = position_data["posY"]
        calculated_position.posZ = position_data["posZ"]
        calculated_position.rotX = signal_data["rotX"]

        self.signal_datastore.update_position(signal_id, additional_data, position_data, calculated_position)

        return calculated_position,additional_data
