"""
super-class for data passed from the receiver
"""
from magic_computer_comms.data_model.position_data import PositionData

import json

class OptionedSignalData(object):
    signal_data: PositionData = None
    optional_data: dict = None
    raw_data: dict = None

    def __init__(self, jsonString: str = ""):
        if jsonString != "":
            self.__dict__ = json.loads(jsonString)
            self.raw_data = self.__dict__


    # def __init__(self, signal_data: dict, optional_data: dict):
    #     self.signal_data = signal_data
    #     self.optional_data = optional_data
