"""
In-Memory Database for storing signal position data
"""

import threading

class SignalDatastore(object):
    """
    Creates a signal datastore instance
    """
    datstore_lock = threading.Lock()
    sensor_position_lock = threading.Lock()

    def __init__(self):
        self.__datastore = {}
        self.__sensor_position = {}
        self.__sensor_position["posX"] = 0
        self.__sensor_position["posY"] = 0
        self.__sensor_position["posZ"] = 0
        self.__sensor_position["rotX"] = 0
        self.__sensor_position["rotY"] = 0
        self.__sensor_position["rotZ"] = 0

    def new_signal(self, name) -> None:
        """
        Adds a new signal to the datastore
        """
        self.datstore_lock.acquire()
        if not name in self.__datastore:
            self.__datastore[name] = []
        self.datstore_lock.release()

    def update_sensor_position(self, position_data: dict) -> None:
        """
        Updates whole or partial position data for the sensor
        """
        keys = position_data.keys()

        self.sensor_position_lock.acquire()
        for key in keys:
            self.__sensor_position[key] = position_data[key]
        self.sensor_position_lock.release()

    def get_sensor_position(self) -> dict:
        """
        Gets latest position data
        """

        self.sensor_position_lock.acquire()
        ret_val: dict = self.__sensor_position
        self.sensor_position_lock.release()

        return ret_val

    def update_position(self, name, receiver_data, calculated_position) -> None:
        """
        Adds new position data.

        receiver_data is a dictionary:
        {id, posX, posY, posZ, rotX, rotY, rotZ}

        calculated_position is a dictionary:
        {posX, posY, posZ}
        """
        if not name in self.__datastore:
            self.new_signal(name)

        self.datstore_lock.acquire()
        self.__datastore[name].append((receiver_data, calculated_position))
        self.datstore_lock.release()

    def get_latest_position(self, name) -> dict:
        """
        Gets the last position.  Data is returned as a tuple of
        the calculated position, and the receiver id and position that detected it
        """

        self.datstore_lock.acquire()
        data_length = len(self.__datastore[name])
        latest_position = self.__datastore[name][data_length - 1]
        self.datstore_lock.release()

        return latest_position

    def get_position_data(self, name) -> dict:
        """
        Returns the entire array of position data for a signal
        """
        self.datstore_lock.acquire()
        position_data = self.__datastore[name]
        self.datstore_lock.release()

        return position_data

    def get_signal_names(self) -> set:
        """
        Returns the names of every known signal
        """
        self.datstore_lock.acquire()
        signal_name = self.__datastore.keys()
        self.datstore_lock.release()

        return signal_name
