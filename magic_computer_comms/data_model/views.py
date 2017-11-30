"""
Super-type of all views
"""
import os

class Views(object):
    """
    All views inherit from this class for their method list
    """
    def __init__(self, options: dict):
        self.options = options

    def update_view(self, pertinent_signal: str, refined_position: dict) -> None:
        """
        Provides logic for formatting requests
        """
        if os.environ["magic_computer_debug"] == "true":
            xpos = refined_position["posX"]
            ypos = refined_position["posY"]
            zpos = refined_position["posZ"]

            pos_string = str(xpos) + ", " + str(ypos) + ", " + str(zpos)

            print("Sending position update for signal " + pertinent_signal + " of " + pos_string)
