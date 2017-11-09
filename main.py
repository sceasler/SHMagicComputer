"""
Main entry point.  Defines services and launches app.
"""
from magic_computer_comms.startup import Startup

APP = Startup()

APP.configure()

APP.start()
