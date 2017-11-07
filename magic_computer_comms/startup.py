"""
Initiates app startup
"""
import json
import re
from magic_computer_comms.io.view_comm_server import ThreadedServer
from magic_computer_comms.data_model.views import Views

class Startup(object):
    """
    Provides methods for startup of application
    """
    server: ThreadedServer
    parser: None
    algo: None
    receiver: None
    discriminator: None

    def __init__(self):
        #working_dir = sys.argv[0]
        with open('appsettings.json') as data_file:
            self.environment = json.load(data_file)

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

        parser_class_name = self.environment["view"]["parser"] + "View"

        parser_str = self.__to_snake_case__(parser_class_name)

        ret_val = self.__string_import__("views." + parser_str + "." + parser_class_name)

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
        ######Configuring the viewer######
        host: str = self.environment["view"]["host"]
        port: int = self.environment["view"]["port"]
        klass = self.__load_view__()

        self.parser = klass(host=host, port=port)

        self.server = ThreadedServer(host, port, self.parser)
        ##################################

        #####Configuring the df algo#####
        self.algo = None
        #################################

        ##Configuring the discriminator##
        self.discriminator = None
        #################################

        #####Configuring the receiver####
        self.receiver = None
        #################################

        return (self.parser, self.algo, self.discriminator, self.receiver)

    def start(self):
        """
        starts all services
        """
        self.server.listen()
