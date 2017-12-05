"""
Listens for data from clients and sends input to processor
"""

import socket
import threading

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
        threading.Thread(target=self.listen_to_client).start()

    def listen_to_client(self):
        """
        Loops through receiving data to pass to parser and processor
        """
        size = 1024
        while True:
            raw_data = self.sock.recv(size)
            #data = raw_data.decode()
            self.processor(raw_data)

            #(xpos, ypos, zpos, xrot, yrot, zrot) = self.parser.parseView(data)
            #processor not defined yet
