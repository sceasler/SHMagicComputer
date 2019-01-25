import asyncio
import os
import sys
from telnetlib import Telnet

class TelnetClient(object):
    """
    class for connecting to a telnet server
    """
    def __init__(self, host: str, port: int, timeout: int = 2):
        self.host: str = host
        self.port: int = port
        
        if os.environ["magic_computer_debug"] == "true":
            print("Connecting to " + host + " on port " + str(port))

        self.tn: Telnet = Telnet(host, port, timeout)

    def send(self, message: str) -> str:
        if os.environ["magic_computer_debug"] == "true":
            print("Sending " + message)
        
        self.tn.write(message)

        return self.tn.read_all()

    async def send_async(self, message: str) -> str:
        return await asyncio.wait(self.send(message))

    def shutdown(self) -> None:
        self.tn.close()

    def telnet_object(self) -> None:
        return self.tn

