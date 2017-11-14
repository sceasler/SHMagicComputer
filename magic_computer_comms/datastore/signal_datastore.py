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

        receiver_data is a dictionary:
        {id, posX, posY, posZ, rotX, rotY, rotZ}

        calculated_position is a dictionary:
        {posX, posY, posZ}
        """
        if not name in self.__datastore:
            self.new_signal(name)

        self.__datastore[name].append((receiver_data, calculated_position))

    def get_latest_position(self, name):
        """
        Gets the last position.  Data is returned as a tuple of
        the calculated position, and the receiver id and position that detected it
        """
        data_length = len(self.__datastore[name])
        return self.__datastore[name][data_length - 1]

    def get_position_data(self, name):
        """
        Returns the entire array of position data for a signal
        """
        return self.__datastore[name]

    def get_signal_names(self):
        """
        Returns the names of every known signal
        """

        return self.__datastore.keys()
