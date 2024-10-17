from enum import Enum

class Color(Enum):
    BLUE = 1
    YELLOW = 2
    RED = 3
    GREEN = 4
    

class Object:
    def __init__(self, object_id, size, color):
        self.id = object_id
        self.size = size
        self.color = color
        self.bin_id = None
    
    def add_bin_id(self, bin_id):
        self.bin_id = bin_id