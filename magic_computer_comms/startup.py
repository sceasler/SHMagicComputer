"""
Initiates app startup
"""
import json
import re
import os
import time
from typing import Callable
from typing import Dict
from typing import List
from magic_computer_comms.data_model.listener_subscriber import ListenerSubscriber
from magic_computer_comms.data_model.views import Views
from magic_computer_comms.data_model.locators import Locators
from magic_computer_comms.data_model.receivers import Receivers
from magic_computer_comms.controller.controller import Controller
from magic_computer_comms.data_model.algos import Algos
from magic_computer_comms.data_model.discriminators import Discriminators
from magic_computer_comms.datastore.signal_datastore import SignalDatastore
from magic_computer_comms.io.listener import Listener


class Startup(object):
    """
    Provides methods for startup of application
    """
    views: List[Views]
    algo: Algos
    receivers: List[Receivers]
    discriminator: Discriminators
    locators: List[Locators]
    controller: Controller
    listener: Listener
    listener_callbacks: Dict[str, Callable[[str], None]]
    datastore: SignalDatastore

    def __init__(self):
        #working_dir = sys.argv[0]
        self.listener = None
        self.views = list()
        self.receivers = list()
        self.locators = list()
        self.listener_callbacks = dict()

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

    def __register_for_listener(self, module: dict, klass: ListenerSubscriber):
        if "listener_keywords" in module:
            for keyword in module["listener_keywords"]:
                self.listener_callbacks.update({keyword : klass.process_message})

                if os.environ["magic_computer_debug"] == "true":
                    print("Binding keyword '" + keyword + "' to module '" + module["name"] + "'")

    def __configure_viewers(self):
        ######Configuring the viewers######
        for view in self.environment["views"]:
            klass: Views = self.__load_view__(view["type"])

            if "options" in view:
                options = view["options"]
            else:
                options = None

            self.views.append(klass(options))
        ##################################

    def __configure_algos(self):
        #####Configuring the df algos#####
        algo = self.environment["algo"]

        klass: Algos = self.__load_algo__(algo["type"])

        if "options" in algo:
            options = algo["options"]
        else:
            options = None

        self.algo: Algos = klass(self.datastore, options)

        self.__register_for_listener(algo, self.algo)
        #################################

    def __confgiure_discriminators(self):
        ##Configuring the discriminators##
        discriminator = self.environment["discriminator"]
        klass: Discriminators = self.__load_discriminator__(discriminator["type"])

        if "options" in discriminator:
            options = discriminator["options"]
        else:
            options = None

        self.discriminator = klass(self.datastore, options)

        self.__register_for_listener(discriminator, self.discriminator)
        #################################

    def __configure_locators(self):
        #####Configuring the locators######
        for locator in self.environment["locators"]:
            klass: Locators = self.__load_locator__(locator["type"])

            if "options" in locator:
                options = locator["options"]
            else:
                options = None

            locator_inst = klass(self.datastore, options)

            self.locators.append(locator_inst)

            self.__register_for_listener(locator, locator_inst)
        ##################################

    def __configure_receivers(self):
        #####Configuring the receivers####
        for receiver in self.environment["receivers"]:
            klass = self.__load_receiver__(receiver["type"])

            if "options" in receiver:
                options = receiver["options"]
            else:
                options = None

            receiver_inst = klass(self.controller, options)

            self.receivers.append(receiver_inst)

            self.__register_for_listener(receiver, receiver_inst)
        #################################

    def configure(self) -> (Receivers, Locators, Discriminators, Algos, Views):
        """
        configures services
        """

        self.datastore = SignalDatastore()

        self.__configure_viewers()

        self.__configure_algos()

        self.__confgiure_discriminators()

        self.controller: Controller = Controller(self.datastore, self.discriminator, self.algo, self.views)

        self.__configure_locators()

        self.__configure_receivers()

        return (self.receivers, self.locators, self.discriminator, self.algo, self.views)

    def start(self):
        """
        starts all services
        """

        for receiver in self.receivers:
            receiver.start()

        for locator in self.locators:
            locator.start()

        callback_count = len(self.listener_callbacks)

        if callback_count > 0:
            self.listener = Listener(self.environment["listener_port"], self.listener_callbacks)
            self.listener.start()

        while True:
            time.sleep(7200)
