"""
Initiates app startup
"""
import json
import re
import os
import time
from magic_computer_comms.data_model.views import Views
from magic_computer_comms.data_model.locators import Locators
from magic_computer_comms.data_model.receivers import Receivers
from magic_computer_comms.controller.controller import Controller
from magic_computer_comms.data_model.algos import Algos
from magic_computer_comms.data_model.discriminators import Discriminators
from magic_computer_comms.datastore.signal_datastore import SignalDatastore

class Startup(object):
    """
    Provides methods for startup of application
    """
    view: Views
    algo: None
    receiver: Receivers
    discriminator: None
    locator: Locators
    controller: Controller

    def __init__(self):
        #working_dir = sys.argv[0]
        with open('appsettings.json') as data_file:
            self.environment = json.load(data_file)

        if "debug" in self.environment and self.environment["debug"] is True:
            os.environ["magic_computer_debug"] = "true"
        else:
            os.environ["magic_computer_debug"] = "false"

    def get_environment(self):
        """
        returns data from appsettings.json
        """
        return self.environment

    @staticmethod
    def __to_snake_case__(item):
        temp_string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', item)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', temp_string).lower()

    def __load_view__(self):
        ret_val: Views

        parser_class_name = self.environment["view"]["type"] + "View"

        parser_str = self.__to_snake_case__(parser_class_name)

        ret_val = self.__string_import__("views." + parser_str + "." + parser_class_name)

        return ret_val

    def __load_locator__(self):
        ret_val: Locators

        locator_class_name = self.environment["locator"]["type"] + "Locator"

        locator_str = self.__to_snake_case__(locator_class_name)

        ret_val = self.__string_import__("locators." + locator_str + "." + locator_class_name)

        return ret_val

    def __load_receiver__(self):
        ret_val: Receivers

        receiver_class_name = self.environment["receiver"]["type"] + "Receiver"
        receiver_str = self.__to_snake_case__(receiver_class_name)
        ret_val = self.__string_import__("receivers." + receiver_str + "." + receiver_class_name)

        return ret_val

    def __load_algo__(self):
        ret_val: Algos

        algo_class_name = self.environment["algo"]["type"] + "Algo"
        algo_str = self.__to_snake_case__(algo_class_name)
        ret_val = self.__string_import__("algos." + algo_str + "." + algo_class_name)

        return ret_val

    def __load_discriminator__(self):
        ret_val: Discriminators

        discrim_class_name = self.environment["discriminator"]["type"] + "Discriminator"
        discrim_str = self.__to_snake_case__(discrim_class_name)
        ret_val = self.__string_import__("discriminators." + discrim_str + "." + discrim_class_name)

        return ret_val

    @staticmethod
    def __string_import__(class_path: str):
        components = class_path.split('.')
        mod = __import__(components[0] + "." + components[1])
        for comp in components[1:]:
            mod = getattr(mod, comp)

        return mod

    def configure(self):
        """
        configures services
        """
        #######Initialize Datastore#######
        datastore = SignalDatastore()
        ##################################

        ######Configuring the viewer######
        klass = self.__load_view__()

        self.view = klass(self.environment["view"]["options"])
        ##################################

        #####Configuring the df algo#####
        klass = self.__load_algo__()

        self.algo = klass(datastore)
        #################################

        ##Configuring the discriminator##
        klass = self.__load_discriminator__()

        self.discriminator = klass(datastore)
        #################################

        #####Configuring the locator######
        klass = self.__load_locator__()

        self.locator = klass(self.environment["locator"]["options"])
        ##################################

        ####Configuring the controller###
        self.controller: Controller = Controller(self.locator, self.discriminator, self.algo, self.view)
        #################################

        #####Configuring the receiver####
        klass = self.__load_receiver__()

        self.receiver = klass(self.controller, self.environment["receiver"]["options"])
        #################################

        return (self.receiver, self.locator, self.discriminator, self.algo, self.view)

    def start(self):
        """
        starts all services
        """
        self.controller.start()
        self.receiver.start()

        while True:
            time.sleep(20)
