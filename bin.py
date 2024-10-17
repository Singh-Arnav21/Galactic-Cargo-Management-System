from avl import AVLTree

class Bin:
    def __init__(self, bin_id, capacity):
        self.id = bin_id
        self.capacity = capacity
        self.remaining_capacity = capacity
        self.obj_stored = AVLTree()