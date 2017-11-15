"""
Implementation of the viewer for Microsoft HoloLens
"""

import json
import os
from magic_computer_comms.data_model.views import Views
from magic_computer_comms.io.comm_sender import ThreadedSender

class HoloLensView(Views):
    """
    Provides formatting data for sending data to the HoloLens
    """
    def __init__(self, options):
        super(HoloLensView, self).__init__(options)

        host = options["view_host"]
        port = int(options["view_port"])

        self.sender = ThreadedSender(host, port)

        if os.environ['magic_computer_debug'] == "true":
            print("set up to use view at " + host + ":" + str(port) + " using UDP")

    def update_view(self, pertinent_signal, refined_position):
        super(HoloLensView, self).update_view(pertinent_signal, refined_position)

        refined_position["signalId"] = pertinent_signal
        refined_position["messageType"] = "PosUpdate"

        self.sender.send_to_client(json.dumps(refined_position).encode('utf_8'))
