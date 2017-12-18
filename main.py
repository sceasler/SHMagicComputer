"""
Main entry point.  Defines services and launches app.
"""
from magic_computer_comms.startup import Startup

APP = Startup()

(RECEIVERS, LOCATORS, DISCRIMINATOR, ALGO, VIEWERS) = APP.configure()

#Any additional configurations for the returned components can go here

APP.start()
