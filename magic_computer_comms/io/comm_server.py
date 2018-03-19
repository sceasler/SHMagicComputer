"""
Listens for data from clients and sends input to processor
"""

import socket
import threading
import os

class ThreadedServer(object):
    """
    Listens on UDP port for client communication
    Sends raw data to parser
    Passes parsed data to defined processor
    """

    def __init__(self, host, port, processor):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.processor = processor

    def listen(self):
        """
        Starts thread that listens for communication on UDP port
        """
        if os.environ["magic_computer_debug"] == "true":
            print("Creating threaded listener")

        threading.Thread(target=self.__listen_to_client).start()

    def __listen_to_client(self):
        """
        Loops through receiving data to pass to parser and processor
        """
        size = 1024
        while True:
            raw_data = self.sock.recv(size)

            if os.environ["magic_computer_debug"] == "true":
                print("Creating listening processor thread")

            # thread = threading.Thread(target=self.processor, args=[raw_data])
            # thread.

            threading.Thread(target=self.processor, args=[raw_data]).start()
