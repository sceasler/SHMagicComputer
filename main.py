"""
Main entry point.  Defines services and launches app.
"""
from magic_computer_comms.startup import Startup

APP = Startup()

(RECEIVER, LOCATOR, DISCRIMINATOR, ALGO, VIEWER) = APP.configure()

APP.start()
