"""
super-class for data passed from the receiver
"""
import json

class OptionedSignalData(object):
    signal_data = None
    optional_data = None

    def __init__(self, jsonString: str = ""):
        if jsonString != "":
            self.__dict__ = json.loads(jsonString)

    # def __init__(self, signal_data: dict, optional_data: dict):
    #     self.signal_data = signal_data
    #     self.optional_data = optional_data
