from magic_computer_comms.data_model.views import Views

class HoloLensView(Views):
    def update_view(self, pertinent_signal, refined_position):
        xpos = str(refined_position[0])
        ypos = str(refined_position[1])
        zpos = str(refined_position[2])

        self.sender.send_to_client_async("POSUPDATE|" + pertinent_signal + "|" + xpos + "," + ypos + "," + zpos)
