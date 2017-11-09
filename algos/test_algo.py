from magic_computer_comms.data_model.algos import Algos

class TestAlgo(Algos):
    def refine_position(self, signal_id, position_data):
        return (0, 0, 0)
