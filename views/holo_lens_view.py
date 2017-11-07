"""
Provides the interface for interacting with
The Microsoft Hololens
"""
from magic_computer_comms.data_model.views import Views
from magic_computer_comms.io.view_request_types import RequestType

class HoloLensView(Views):
    """
    Defines the interface for the HoloLens
    """

    def __init__(self, host: str, port: int):
        super(HoloLensView, self).__init__(viewType="HoloLensView", host=host, port=port)

    def parse_view(self, message: str):
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
