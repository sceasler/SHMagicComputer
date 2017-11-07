"""
RequestType enumeration
"""

from enum import Enum

class RequestType(Enum):
    """
    RequestType enumeration for defining what is to be
    requested of the client
    """
    position = 1
    rotation = 2
    positionandrotation = 3
