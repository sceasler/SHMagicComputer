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
        self.server.send("\n\r")
        self.server.send(init_string)
        self.server.send(tune_string)
        self.server.send("LOB?;\n\r")

    def send_to_controller(self, signal_data: str):
        #take received data  and convert to OptionedsignalData

        #parse signal_data into json

        string_data = signal_data.split(',')

        data_object = {
            'Bearing': string_data[0],
            'STD': string_data[1],
            'SignalStrength': string_data[2], 
            'IntegrationTime': string_data[3],
            'UTC' : string_data[4],
            'Lat': string_data[5],
            'Lon': string_data[6],
            'Heading': string_data[7],
            'Speed': string_data[8],
            'OneValid': string_data[9],
            "CompassHdg": string_data[10]
        }

        ret_val = OptionedSignalData(json.dumps(data_object))

        optional_data = {'signal_strength': str(ret_val.raw_data["signalStrength"])}

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

    async def data_push(self):
        """
        Gets latest DF information from receiver
        """

        while True:
            server_send_task = asyncio.create_task(self.server.send_async("DFI?;\n\r"))

            dfi: str = await server_send_task
            self.send_to_controller(dfi)
            await asyncio.sleep(1.0)

    def start(self):
        """
        Begins to listen to receive events
        """

        asyncio.run(self.data_push())        

        #threading.Thread(target=self.data_push).start()
