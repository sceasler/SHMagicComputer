"""
provides interface for retrieving
positional data from the DF-A0047 antenna
"""

import os
import time
import threading
import visa
from magic_computer_comms.data_model.locators import Locators
from magic_computer_comms.datastore.signal_datastore import SignalDatastore

class Dfa0047Locator(Locators):
    """
    Defines the interface for the DF-A0047 antenna location
    """

    def __init__(self, datastore: SignalDatastore, options):
        super(Dfa0047Locator, self).__init__(datastore, options)

        self.resource_manager = visa.ResourceManager("C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\TekVISA\\Bin\\Visa32.dll")
        instruments = self.resource_manager.list_resources()
        self.inst = self.resource_manager.open_resource(instruments[0])

    def __run_data_grab(self):
        while True:
            data_string: str = self.inst.query("SYST:ANT:DATA?")

            data_return = {}

            azimuth = data_string.split(",")[1]
            declination = self.inst.query("SYST:ANT:DECL?")

            data_return["rotX"] = int(float(azimuth))
            data_return["rotY"] = int(float(declination.strip()))

            self.datastore.update_sensor_position(data_return)

            if os.environ["magic_computer_debug"] == "true":
                print(self.datastore.get_sensor_position())

            time.sleep(.25)

    def start(self):
        threading.Thread(target=self.__run_data_grab).start()
