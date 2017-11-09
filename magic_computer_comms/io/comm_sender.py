"""
Sends generic data via UDP
"""

import socket
import threading

class ThreadedSender(object):
    """
    Sends UDP data
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_to_client(self, message: str):
        """
        Synchronous send of message to host
        """

        self.sock.sendto(message.encode('utf_8'), (self.host, self.port))

    def send_to_client_async(self, message: str):
        """
        Asynchronous send of message to host
        """
        threading.Thread(target=self.send_to_client, args=[message]).start()
