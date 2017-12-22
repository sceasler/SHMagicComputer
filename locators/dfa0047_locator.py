"""
provides interface for retrieving
positional data from the DF-A0047 antenna
"""

import os
import subprocess
import time
import threading
from pyvisa.errors import VisaIOError
import visa
from magic_computer_comms.data_model.locators import Locators
from magic_computer_comms.datastore.signal_datastore import SignalDatastore

class Dfa0047Locator(Locators):
    """
    Defines the interface for the DF-A0047 antenna location
    """

    def __init__(self, datastore: SignalDatastore, options):
        super(Dfa0047Locator, self).__init__(datastore, options)

        self.signal_vu_path = "C:\\Program Files\\Tektronix\\SignalVu-PC\\SignalVu-PC.exe"
        self.resource_manager_path = "C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\TekVISA\\Bin\\Visa32.dll"
        self.resource_manager = None
        self.inst = None

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
        if os.environ["magic_computer_debug"] == "true":
            print("Launching SignalVu-PC")

        p = subprocess.Popen([self.signal_vu_path])

        self.resource_manager = visa.ResourceManager(self.resource_manager_path)

        if os.environ["magic_computer_debug"] == "true":
            print("Waiting for instrument to load")

        instruments = None

        while not isinstance(instruments, tuple):
            instruments = self.resource_manager.list_resources()
            time.sleep(.5)

        start_continue = False
        while not start_continue:
            try:
                time.sleep(5)
                self.inst = self.resource_manager.open_resource(instruments[0])
                start_continue = True
            except VisaIOError:
                start_continue = False

        if os.environ["magic_computer_debug"] == "true":
            print("Instruments loaded. Connecting antenna")

        self.inst.write('SYST:ANT:SEL Alaris DF-A0047')
        self.inst.write('SYST:ANT:CONN 1')

        threading.Thread(target=self.__run_data_grab).start()
