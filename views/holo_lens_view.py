"""
Implementation of the viewer for Microsoft HoloLens
"""

import json
import os
from magic_computer_comms.data_model.views import Views

class HoloLensView(Views):
    """
    Provides formatting data for sending data to the HoloLens
    """
    def update_view(self, pertinent_signal, refined_position):
        super(HoloLensView, self).update_view(pertinent_signal, refined_position)

        refined_position["signalId"] = pertinent_signal
        refined_position["messageType"] = "PosUpdate"

        self.sender.send_to_client_async(json.dumps(refined_position).encode('utf_8'))
