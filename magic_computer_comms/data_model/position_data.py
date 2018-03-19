
import json

class MetaPositionData(object):
    posX: str = None
    posY: str = None
    posZ: str = None
    rotX: str = None
    rotY: str = None
    rotZ: str = None


"""
Describes a position in 3-dimensional space
"""
class PositionData(MetaPositionData):
    def __init__(self, json_string: str = ''):
        if json_string != '':
            self.load_from_json(json_string)

    def load_from_json(self, json_string: str):
        self.__dict__ = json.loads(json_string)

    def initialize(self):
        self.posX = '0'
        self.posY = '0'
        self.posZ = '0'
        self.rotX = '0'
        self.rotY = '0'
        self.rotZ = '0'

    def update_position(self, updated_position: MetaPositionData):
        if updated_position.posX != None:
            self.posX = updated_position.posX

        if updated_position.posY != None:
            self.posX = updated_position.posY

        if updated_position.posZ != None:
            self.posX = updated_position.posZ

        if updated_position.rotX != None:
            self.posX = updated_position.rotX

        if updated_position.rotY != None:
            self.posX = updated_position.rotY            

        if updated_position.posZ != None:
            self.posX = updated_position.posZ

    def __getitem__(self, key):
        if key == "posX":
            return self.posX
        
        if key == "posY":
            return self.posY

        if key == "posZ":
            return self.posZ

        if key == "rotX":
            return self.rotX

        if key == "rotY":
            return self.rotY

        if key == "rotZ":
            return self.rotZ

    def __setitem__(self, key, value):
        if key == "posX":
            self.posX = value
        
        if key == "posY":
            self.posY = value

        if key == "posZ":
            self.posZ = value

        if key == "rotX":
            self.rotX = value

        if key == "rotY":
            self.rotY = value

        if key == "rotZ":
            self.rotZ = value