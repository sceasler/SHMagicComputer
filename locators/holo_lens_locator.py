"""
Provides the interface for interacting with
The Microsoft Hololens for location
"""

from magic_computer_comms.data_model.locators import Locators
from magic_computer_comms.io.locator_request_types import RequestType

class HoloLensLocator(Locators):
    """
    Defines the interface for the HoloLens location service
    """

    def __init__(self, r_host: str, r_port: int, s_host: str, s_port: int):
        super(HoloLensLocator, self).__init__(r_host=r_host, r_port=r_port, s_host=s_host, s_port=s_port)

    def parse_locator(self, message: str):
        message_split = message.split(sep='|')

        if message_split[0] == 'CLIENTPOSITION':
            return (message_split[1]. messageSplit[2], message_split[3], None, None, None)
        elif message_split[1] == 'CLIENTROTATION':
            return (None, None, None, message_split[1], message_split[2], message_split[3])

    def send_request(self, request_type: int, parameters):
        requests = list()

        if request_type == RequestType.position:
            requests.append("ASKPOSITION|null%0%0%0")
        elif request_type == RequestType.rotation:
            requests.append("ASKROTATION|null%0%0%0")
        elif request_type == RequestType.positionandrotation:
            requests.append("ASKPOSITION|null%0%0%0")
            requests.append("ASKROTATION|null%0%0%0")

        for request in requests:
            self.sender.send_to_client_async(request)
