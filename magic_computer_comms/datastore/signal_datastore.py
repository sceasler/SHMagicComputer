"""
In-Memory Database for storing signal position data
"""

import threading

class SignalDatastore(object):
    """
    Creates a signal datastore instance
    """
    lock = threading.Lock()

    def __init__(self):
        self.__datastore = {}

    def new_signal(self, name):
        """
        Adds a new signal to the datastore
        """
        self.lock.acquire()
        if not name in self.__datastore:
            self.__datastore[name] = []
        self.lock.release()

    def update_position(self, name, receiver_data, calculated_position):
        """
        Adds new position data.

        receiver_data is a dictionary:
        {id, posX, posY, posZ, rotX, rotY, rotZ}

        calculated_position is a dictionary:
        {posX, posY, posZ}
        """
        if not name in self.__datastore:
            self.new_signal(name)
            
        self.lock.acquire()
        self.__datastore[name].append((receiver_data, calculated_position))
        self.lock.release()

    def get_latest_position(self, name):
        """
        Gets the last position.  Data is returned as a tuple of
        the calculated position, and the receiver id and position that detected it
        """

        self.lock.acquire()
        data_length = len(self.__datastore[name])
        latest_position = self.__datastore[name][data_length - 1]
        self.lock.release()

        return latest_position

    def get_position_data(self, name):
        """
        Returns the entire array of position data for a signal
        """
        self.lock.acquire()
        position_data = self.__datastore[name]
        self.lock.release()

        return position_data

    def get_signal_names(self):
        """
        Returns the names of every known signal
        """
        self.lock.acquire()
        signal_name = self.__datastore.keys()
        self.lock.release()

        return signal_name
