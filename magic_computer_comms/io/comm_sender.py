"""
Sends generic data via UDP
"""

import asyncio
import socket
#import threading

class ThreadedSender(object):
    """
    Sends UDP data
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_to_client(self, message):
        """
        Synchronous send of message to host
        """

        self.sock.sendto(message, (self.host, self.port))

    def send_to_client_async(self, message):
        """
        Asynchronous send of message to host
        """
        yield from asyncio.Task(self.send_to_client(message))
