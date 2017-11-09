"""
Implementation of the viewer for Microsoft HoloLens
"""

import json
from magic_computer_comms.data_model.views import Views

class HoloLensView(Views):
    """
    Provides formatting data for sending data to the HoloLens
    """
    def update_view(self, pertinent_signal, refined_position):
        xpos = str(refined_position[0])
        ypos = str(refined_position[1])
        zpos = str(refined_position[2])

        message = {}
        message["posX"] = xpos
        message["posY"] = ypos
        message["posZ"] = zpos
        message["signalId"] = pertinent_signal
        message["messageType"] = "PosUpdate"

        self.sender.send_to_client_async(json.dumps(message))
