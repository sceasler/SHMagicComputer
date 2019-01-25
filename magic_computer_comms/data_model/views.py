"""
Super-type of all views
"""
import json
import os
from magic_computer_comms.data_model.position_data import PositionData

class Views(object):
    """
    All views inherit from this class for their method list
    """
    def __init__(self, options: dict):
        self.options = options

    def update_view(self, pertinent_signal: str, refined_position: PositionData, additional_data: dict) -> None:
        """
        Provides logic for formatting requests
        """
        if os.environ["magic_computer_debug"] == "true":
            xpos = refined_position.posX
            ypos = refined_position.posY
            zpos = refined_position.posZ
            xrot = refined_position.rotX
            yrot = refined_position.rotY
            zrot = refined_position.rotZ

            pos_string = str(xpos) + ", " + str(ypos) + ", " + str(zpos) + ", " + str(xrot) + ", " + str(yrot) + ", " + str(zrot)

            print("Sending position update for signal " + pertinent_signal + " of " + pos_string)
            print("optional data: " + json.dumps(additional_data))
