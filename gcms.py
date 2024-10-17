from bin import Bin
from avl import AVLTree
from object import Object, Color
from node import Node
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        self.AVL_container = AVLTree()
        self.AVL_obj = AVLTree()
        self.AVL_bin = AVLTree()
        

    def add_bin(self, bin_id, capacity, to_add = None):
        if to_add:
            temp = to_add.access
        else:
            temp = Bin(bin_id, capacity)
        ptr1_to_bin = Node(temp, capacity)
        ptr2_to_bin = Node(temp, capacity)
        
        attach_at = self.AVL_container.find_key(temp.remaining_capacity, False)
        if attach_at is None:
            attach_at = Node(AVLTree(), capacity)
            self.AVL_container.insert(attach_at, False)
        attach_at.access.insert(ptr1_to_bin, True)
        if to_add is None:
            self.AVL_bin.insert(ptr2_to_bin, True)


    def add_object(self, object_id, size, color):
        temp = Object(object_id, size, color)
        ptr1_to_obj = Node(temp, size)
        ptr2_to_obj = Node(temp, size)
        
        ptr_to_bin = None
        container = None
        
        if temp.color == Color.BLUE:
            container = self.AVL_container.greater_or_equal(ptr1_to_obj)
            if container is None:
                raise NoBinFoundException
            
            ptr_to_bin = container.access.find_min()
                
            ptr_to_bin.access.obj_stored.insert(ptr1_to_obj, True)

        elif temp.color == Color.YELLOW:
            container = self.AVL_container.greater_or_equal(ptr1_to_obj)
            if container is None:
                raise NoBinFoundException
            
            ptr_to_bin = container.access.find_max()

            ptr_to_bin.access.obj_stored.insert(ptr1_to_obj, True)

        elif temp.color == Color.RED:
            container = self.AVL_container.find_max()
            
            if container.remaining_capacity < temp.size:
                raise NoBinFoundException
            
            ptr_to_bin = container.access.find_min()

            ptr_to_bin.access.obj_stored.insert(ptr1_to_obj, True)

        else:
            container = self.AVL_container.find_max()
            
            if container.remaining_capacity < temp.size:
                raise NoBinFoundException
            
            ptr_to_bin = container.access.find_max()

            ptr_to_bin.access.obj_stored.insert(ptr1_to_obj, True)

        temp.add_bin_id(ptr_to_bin.access.id)
        self.AVL_obj.insert(ptr2_to_obj, True)
        
        ptr_to_bin.access.remaining_capacity -= temp.size
        ptr_to_bin.remaining_capacity -= temp.size
        
        item_1 = container.access.delete_by_id(ptr_to_bin.access.id)
        
        if container.access.root is None:
            self.AVL_container.delete_by_cap(container.remaining_capacity)
            
        self.add_bin(ptr_to_bin.access.id, ptr_to_bin.remaining_capacity, ptr_to_bin)


    def delete_object(self, object_id):
        ptr_to_obj = self.AVL_obj.find_key(object_id, True)
        if ptr_to_obj is None:
            return None
        bin_id = ptr_to_obj.access.bin_id
        
        ptr_to_bin = self.AVL_bin.find_key(bin_id, True)
        bin_capacity = ptr_to_bin.access.remaining_capacity
        
        container = self.AVL_container.find_key(bin_capacity, False)
        ptr_to_bin = container.access.find_key(bin_id, True)
        
        ptr_to_bin.access.obj_stored.delete_by_id(object_id)
        ptr_to_bin.access.remaining_capacity += ptr_to_obj.access.size

        item_1 = container.access.delete_by_id(bin_id)
        
        if container.access.root is None:
            self.AVL_container.delete_by_cap(bin_capacity)

        self.add_bin(bin_id, ptr_to_bin.access.remaining_capacity, ptr_to_bin)
        self.AVL_obj.delete_by_id(object_id)
    

    def bin_info(self, bin_id):
        ptr_to_bin = self.AVL_bin.find_key(bin_id, True)
        remaining_capacity = ptr_to_bin.access.remaining_capacity
        objects_stored = ptr_to_bin.access.obj_stored.inorder_traversal(ptr_to_bin.access.obj_stored.root)
        bin_info_tuple = (remaining_capacity, objects_stored)
        
        return bin_info_tuple


    def object_info(self, object_id):
        ptr_to_obj = self.AVL_obj.find_key(object_id, True)
        if ptr_to_obj is None:
            return None
        bin_id = ptr_to_obj.access.bin_id
        
        return bin_id