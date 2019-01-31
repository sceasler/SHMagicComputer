"""
Receiver module for the Blackstone
"""
import asyncio
#import threading
import time
import os
import json
from magic_computer_comms.data_model.receivers import Receivers
from magic_computer_comms.io.telnet_client import TelnetClient
from magic_computer_comms.data_model.optioned_signal_data import OptionedSignalData
from magic_computer_comms.data_model.position_data import PositionData
from magic_computer_comms.controller.controller import Controller

class BlackstoneReceiver(Receivers):
    """
    Blackstone receiver formatter
    """
    def __init__(self, controller: Controller, options):
        super(BlackstoneReceiver, self).__init__(controller, options)

        host = options["receiver_host"]
        port = int(options["receiver_port"])
        bwc = float(options["bandwidth"])
        freq = float(options["frequency"])
        
        init_string: str = "AFC 1;BWC " + str(bwc) + ";AGC 1;DFT 04;DFA 0;DFO 1;\n\r"
        tune_string = "FRQ " + str(freq) + ";\n\r"

        self.server = TelnetClient(host, port)
        self.std_threshold = float(options["std_threshold"])
        self.strength_treshold = float(options["strength_threshold"])
        #self.server.send_void("\n\r")
        bwc_back = self.server.send("BWC?\n\r")
        
        self.server.send(init_string)

        while bwc_back != "BWC 00.010\r\n":
            self.server.send(init_string)
            time.sleep(1)
            bwc_back = self.server.send("BWC?\n\r").decode('ascii')
            if os.environ["magic_computer_debug"] == "true":
                print("received " + bwc_back)


        self.server.send(tune_string)
        self.server.send("LOB?;\n\r")

    def send_to_controller(self, signal_data: str):
        #take received data  and convert to OptionedsignalData

        #parse signal_data into json

        string_data = signal_data.split(',')

        bearing_array = string_data[0].split(' ')

        bearing = float(bearing_array[1])

        #bearing = bearing * -1

        #if bearing < 0:
        #    bearing = 360 + bearing

        data_object = {
            'Bearing': str(bearing),
            'STD': string_data[1],
            'SignalStrength': string_data[2], 
            'IntegrationTime': string_data[3],
            'UTC' : string_data[4],
            'Lat': string_data[5],
            'Lon': string_data[6],
            'Heading': string_data[7],
            'Speed': string_data[8],
            'OneValid': string_data[9],
            "Frequency": string_data[10],
            "CompassHdg": string_data[11]
        }

        ret_val = OptionedSignalData(json.dumps(data_object))

        std_float = float(string_data[1])
        signal_strength = float(string_data[2])

        if std_float <= self.std_threshold and signal_strength >= self.strength_treshold:
            if os.environ["magic_computer_debug"] == "true":
                print("Signal threshold reached")

            optional_data = {
                'signal_strength': str(ret_val.raw_data["SignalStrength"]),
                'standard_deviation': str(ret_val.raw_data["STD"]),
                'integration_time': str(ret_val.raw_data["IntegrationTime"]),
                'heading': str(ret_val.raw_data['Heading'])
            }

            positioned_data = PositionData()
            positioned_data.rotX = str(ret_val.raw_data["Bearing"])

            ret_val.optional_data = optional_data
            ret_val.signal_data = positioned_data

            sensor_position = PositionData()
            sensor_position.posZ = '0'
            sensor_position.posX = ret_val.raw_data['Lon']
            sensor_position.posY = ret_val.raw_data['Lat']
            sensor_position.rotX = ret_val.raw_data['CompassHdg']

            self.controller.datastore.update_sensor_position(sensor_position)

            self.controller.process_signal_detect(ret_val)
        elif os.environ["magic_computer_debug"] == "true":
            print("signal received is below std threshold")
            print("std " + str(std_float))
            print("strength " + str(signal_strength))



    async def data_push(self):
        """
        Gets latest DF information from receiver
        """

        while True:
            #server_send_task = asyncio.create_task(self.server.send_async("DFI?;\n\r"))

            #response = await server_send_task

            response = self.server.send("DFI?;\n\r")

            dfi: str = response.decode('ascii').rstrip()
            self.send_to_controller(dfi)
            await asyncio.sleep(1.0)

    def start(self):
        """
        Begins to listen to receive events
        """

        #response = self.server.send("DFI?;\n\r")

        asyncio.run(self.data_push())        

        #threading.Thread(target=self.data_push).start()
