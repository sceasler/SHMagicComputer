"""
Template for all receiver formatters
"""

from magic_computer_comms.data_model.listener_subscriber import ListenerSubscriber
from magic_computer_comms.controller.controller import Controller

class Receivers(ListenerSubscriber):
    """
    All receiver formatters inherit from here.  This will
    convert data from a receiver into a common format and
    notify the controller of a detect event
    """
    def __init__(self, controller: Controller, options: dict):
        self.controller = controller
        self.options = options

    def start(self) -> None:
        """
        ABSTRACT

        Begins to listen to receive events
        """
        pass
