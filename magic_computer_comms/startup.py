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

    @staticmethod
    def __load_view__(view_type):
        ret_val: Views

        parser_class_name = view_type + "View"
        parser_str = Startup.__to_snake_case__(parser_class_name)
        ret_val = Startup.__string_import__("views." + parser_str + "." + parser_class_name)

        return ret_val

    @staticmethod
    def __load_locator__(locator_type):
        ret_val: Locators

        locator_class_name = locator_type + "Locator"
        locator_str = Startup.__to_snake_case__(locator_class_name)
        ret_val = Startup.__string_import__("locators." + locator_str + "." + locator_class_name)

        return ret_val

    @staticmethod
    def __load_receiver__(receiver_type):
        ret_val: Receivers

        receiver_class_name = receiver_type + "Receiver"
        receiver_str = Startup.__to_snake_case__(receiver_class_name)
        ret_val = Startup.__string_import__("receivers." + receiver_str + "." + receiver_class_name)

        return ret_val

    @staticmethod
    def __load_algo__(algo_type):
        ret_val: Algos

        algo_class_name = algo_type + "Algo"
        algo_str = Startup.__to_snake_case__(algo_class_name)
        ret_val = Startup.__string_import__("algos." + algo_str + "." + algo_class_name)

        return ret_val

    @staticmethod
    def __load_discriminator__(disrim_type):
        ret_val: Discriminators

        discrim_class_name = disrim_type + "Discriminator"
        discrim_str = Startup.__to_snake_case__(discrim_class_name)
        ret_val = Startup.__string_import__("discriminators." + discrim_str + "." + discrim_class_name)

        return ret_val

    @staticmethod
    def __string_import__(class_path: str):
        components = class_path.split('.')
        mod = __import__(components[0] + "." + components[1])
        for comp in components[1:]:
            mod = getattr(mod, comp)

        return mod

    def configure(self) -> (Receivers, Locators, Discriminators, Algos, Views):
        """
        configures services
        """
        #######Initialize Datastore#######
        datastore = SignalDatastore()
        ##################################

        ######Configuring the viewer######
        klass = self.__load_view__(self.environment["view"]["type"])

        if "options" in self.environment["view"]:
            options = self.environment["view"]["options"]
        else:
            options = None

        self.view = klass(options)
        ##################################

        #####Configuring the df algo#####
        klass = self.__load_algo__(self.environment["algo"]["type"])

        if "options" in self.environment["algo"]:
            options = self.environment["algo"]["options"]
        else:
            options = None

        self.algo = klass(datastore, options)
        #################################

        ##Configuring the discriminator##
        klass = self.__load_discriminator__(self.environment["discriminator"]["type"])

        if "options" in self.environment["discriminator"]:
            options = self.environment["discriminator"]["options"]
        else:
            options = None

        self.discriminator = klass(datastore, options)
        #################################

        #####Configuring the locator######
        klass = self.__load_locator__(self.environment["locator"]["type"])

        if "options" in self.environment["locator"]:
            options = self.environment["locator"]["options"]
        else:
            options = None

        self.locator = klass(options)
        ##################################

        ####Configuring the controller###
        self.controller: Controller = Controller(self.locator, self.discriminator, self.algo, self.view)
        #################################

        #####Configuring the receiver####
        klass = self.__load_receiver__(self.environment["receiver"]["type"])

        if "options" in self.environment["receiver"]:
            options = self.environment["receiver"]["options"]
        else:
            options = None

        self.receiver = klass(self.controller, options)
        #################################

        return (self.receiver, self.locator, self.discriminator, self.algo, self.view)

    def start(self):
        """
        starts all services
        """
        self.controller.start()
        self.receiver.start()

        while True:
            time.sleep(7200)
