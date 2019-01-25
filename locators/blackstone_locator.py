from magic_computer_comms.data_model.locators import Locators

class BlackstoneLocator(Locators):
    """
      The position and bearing are in the same message
      Thus location is handled from the receiver
    """
    def start(self) -> None:
        pass

    def process_message(self) -> None:
      pass