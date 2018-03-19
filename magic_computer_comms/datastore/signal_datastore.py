"""
In-Memory Database for storing signal position data
"""

import threading

from magic_computer_comms.data_model.position_data import PositionData

class SignalDatastore(object):
    """
    Creates a signal datastore instance
    """
    datstore_lock = threading.Lock()
    sensor_position_lock = threading.Lock()

    __sensor_position: PositionData

    def __init__(self):
        self.__datastore = {}
        self.__sensor_position = PositionData()
        self.__sensor_position.initialize()

    def new_signal(self, name) -> None:
        """
        Adds a new signal to the datastore
        """
        self.datstore_lock.acquire()
        if not name in self.__datastore:
            self.__datastore[name] = []
        self.datstore_lock.release()

    def update_sensor_position(self, position_data: PositionData) -> None:
        """
        Updates whole or partial position data for the sensor
        """
        self.sensor_position_lock.acquire()
        self.__sensor_position.update_position(position_data)
        self.sensor_position_lock.release()

    def get_sensor_position(self) -> PositionData:
        """
        Gets latest position data
        """

        self.sensor_position_lock.acquire()
        ret_val: PositionData = self.__sensor_position
        self.sensor_position_lock.release()

        return ret_val

    def update_position(self, name, rcv_id: str, receiver_data: PositionData, calculated_position: PositionData) -> None:
        """
        Adds new position data.
        """
        if not name in self.__datastore:
            self.new_signal(name)

        self.datstore_lock.acquire()
        self.__datastore[name].append((rcv_id, receiver_data, calculated_position))
        self.datstore_lock.release()

    def get_latest_position(self, name) -> dict:
        """
        Gets the last position.  Data is returned as a dictionary of
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
