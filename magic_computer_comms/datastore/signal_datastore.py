"""
In-Memory Database for storing signal position data
"""

class SignalDatastore(object):
    """
    Creates a signal datastore instance
    """
    def __init__(self):
        self.__datastore = {}

    def new_signal(self, name):
        """
        Adds a new signal to the datastore
        """
        self.__datastore[name] = []

    def update_position(self, name, receiver_data, calculated_position):
        """
        Adds new position data.

        receiver_data is a tuple:
        (x_position, y_position, z_position, horiz_angle, vert_angle)

        calculated_position is a tuple:
        (x_position, y_position, z_position)
        """
        if not name in self.__datastore:
            self.new_signal(name)

        self.__datastore[name].append((receiver_data, calculated_position))

    def get_latest_position(self, name):
        """
        Gets the last position tuple
        """
        data_length = len(self.__datastore[name])
        return self.__datastore[name][data_length - 1]

    def get_position_data(self, name):
        """
        Returns the entire array of position data for a signal
        """
        return self.__datastore[name]
