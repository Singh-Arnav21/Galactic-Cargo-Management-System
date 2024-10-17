class Node:
    def __init__(self, item = None, capacity = None):
        self.access = item
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0
        self.remaining_capacity = capacity
        