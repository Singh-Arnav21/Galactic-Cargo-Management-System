from node import Node

class AVLTree:

    def __init__(self):
        self.root = None

    def search_key(self, key, use_id):
        if use_id:
            walk = self.root
            while walk:
                if walk.access.id == key:
                    return walk
                elif walk.access.id > key:
                    if walk.left:
                        walk = walk.left
                    else:
                        return walk
                else:
                    if walk.right:
                        walk = walk.right
                    else:
                        return walk
            return walk
            
        else:
            walk = self.root
            while walk:
                if walk.remaining_capacity == key:
                    return walk
                elif walk.remaining_capacity > key:
                    if walk.left:
                        walk = walk.left
                    else:
                        return walk
                else:
                    if walk.right:
                        walk = walk.right
                    else:
                        return walk
            return walk
        
    def find_key(self, key, use_id):
        if use_id:
            walk = self.root
            while walk:
                if walk.access.id == key:
                    return walk
                elif walk.access.id > key:
                    walk = walk.left
                else:
                    walk = walk.right
            return walk
        
        else:
            walk = self.root
            while walk:
                if walk.remaining_capacity == key:
                    return walk
                elif walk.remaining_capacity > key:
                    walk = walk.left
                else:
                    walk = walk.right
            return walk   
        
        
    def insert(self, x, use_id):
        if use_id:
            attach_at = self.search_key(x.access.id, True)
            if not attach_at:
                self.root = x
            else:
                if attach_at.access.id > x.access.id:
                    attach_at.left = x
                else:
                    attach_at.right = x
                x.parent = attach_at
            
                self.recalculate_height(attach_at)
                self.rebalance(attach_at)
                    
        else:
            attach_at = self.search_key(x.remaining_capacity, False)
            if not attach_at:
                self.root = x
            else:
                if attach_at.remaining_capacity > x.remaining_capacity:
                    attach_at.left = x
                else:
                    attach_at.right = x
                x.parent = attach_at
                    
                self.recalculate_height(attach_at)
                self.rebalance(attach_at)
            

    def recalculate_height(self, x):
        x.height = 1 + max(self.height(x.left), self.height(x.right))
            

    def height(self, x):
        if x:
            return x.height
        else:
            return -1
        

    def is_balanced(self, x):
        return abs(self.height(x.left) - self.height(x.right)) <= 1
        

    def tall_child(self, x, favorleft = False):
        if self.height(x.left) + (1 if favorleft else 0) > self.height(x.right):
            return x.left
        else:
            return x.right
            

    def tall_grandchild(self, x):
        y = self.tall_child(x)
        return self.tall_child(y, y == x.left)
        

    def rebalance(self, x):
        while x:
            old_height = x.height
            if not self.is_balanced(x):
                x = self.restructure(self.tall_grandchild(x))
                self.recalculate_height(x.left)
                self.recalculate_height(x.right)
            self.recalculate_height(x)
            if x.height == old_height:
                x = None
            else:
                x = x.parent
        

    def relink(self, parent, child, make_left_child):
        if parent is None:
            if child:
                child.parent = None
        else:
            if make_left_child:
                parent.left = child
            else:
                parent.right = child
            if child:
                child.parent = parent
        

    def rotate(self, x):
        y = x.parent
        z = y.parent
        
        if z is None:
            self.root = x
            x.parent = None
        else:
            self.relink(z, x, y == z.left)
            
        if x == y.left:
            self.relink(y, x.right, True)
            self.relink(x, y, False)
        else:
            self.relink(y, x.left, False)
            self.relink(x, y, True)
            

    def restructure(self, x):
        y = x.parent
        z = y.parent
        
        if (x == y.right) == (y == z.right):
            self.rotate(y)
            return y
        else:
            self.rotate(x)
            self.rotate(x)
            return x


    def find_min(self):
        walk = self.root
        while walk:
            if walk.left:
                walk = walk.left
            else:
                break
        return walk
        
    
    def find_max(self):
        walk = self.root
        while walk:
            if walk.right:
                walk = walk.right
            else:
                break
        return walk       
            

    def greater_or_equal(self, x):
        capacity = x.remaining_capacity
        current = self.root
        greater_or_equal_node = None
    
        while current:
            if current.remaining_capacity < capacity:
                current = current.right
            else:
                greater_or_equal_node = current
                current = current.left
    
        return greater_or_equal_node


    def smallest_in_right_subtree(self, x):
        current = x.right
    
        while current:
            if current.left:
                current = current.left
            else:
                return current
    
        return current


    def delete_by_id(self, key):
        delete_at = self.find_key(key, True)
        if delete_at is None:
            return None
        else:
            return_val = delete_at
            right_smallest_node = self.smallest_in_right_subtree(delete_at)
            if right_smallest_node is None:
                parent = delete_at.parent
                if parent:
                    self.relink(parent, delete_at.left, delete_at == parent.left)

                    delete_at.parent = delete_at.left = delete_at.right = None

                    self.recalculate_height(parent)
                    self.rebalance(parent)    

                else:
                    self.root = delete_at.left
                    if delete_at.left:
                        delete_at.left.parent = None
                        delete_at.left = None
                
            else:
                parent = right_smallest_node.parent
                self.relink(parent, right_smallest_node.right, parent.left == right_smallest_node)
                if delete_at.parent:
                    self.relink(delete_at.parent, right_smallest_node, delete_at == delete_at.parent.left)
                    self.relink(right_smallest_node, delete_at.left, True)
                    self.relink(right_smallest_node, delete_at.right, False)
                
                    delete_at.parent = delete_at.left = delete_at.right = None
                    
                    self.recalculate_height(parent)
                    self.recalculate_height(right_smallest_node)
                    self.rebalance(parent)
                    self.rebalance(right_smallest_node)
                    
                else:
                    self.root = right_smallest_node
                    right_smallest_node.parent = None
                    self.relink(right_smallest_node, delete_at.left, True)
                    self.relink(right_smallest_node, delete_at.right, False)

                    delete_at.left = delete_at.right = None

                    self.recalculate_height(parent)
                    self.recalculate_height(right_smallest_node)
                    self.rebalance(parent)
                    self.rebalance(right_smallest_node)
            return return_val
            
            
    def delete_by_cap(self, key):
        delete_at = self.find_key(key, False)
        if delete_at is None:
            return None
        else:
            return_val = delete_at
            right_smallest_node = self.smallest_in_right_subtree(delete_at)
            if right_smallest_node is None:
                parent = delete_at.parent
                if parent:
                    self.relink(parent, delete_at.left, delete_at == parent.left)

                    delete_at.parent = delete_at.left = delete_at.right = None

                    self.recalculate_height(parent)
                    self.rebalance(parent)    

                else:
                    self.root = delete_at.left
                    if delete_at.left:
                        delete_at.left.parent = None
                        delete_at.left = None
                
            else:
                parent = right_smallest_node.parent
                self.relink(parent, right_smallest_node.right, parent.left == right_smallest_node)
                if delete_at.parent:
                    self.relink(delete_at.parent, right_smallest_node, delete_at == delete_at.parent.left)
                    self.relink(right_smallest_node, delete_at.left, True)
                    self.relink(right_smallest_node, delete_at.right, False)
                
                    delete_at.parent = delete_at.left = delete_at.right = None
                    
                    self.recalculate_height(parent)
                    self.recalculate_height(right_smallest_node)
                    self.rebalance(parent)
                    self.rebalance(right_smallest_node)
                    
                else:
                    self.root = right_smallest_node
                    right_smallest_node.parent = None
                    self.relink(right_smallest_node, delete_at.left, True)
                    self.relink(right_smallest_node, delete_at.right, False)

                    delete_at.left = delete_at.right = None

                    self.recalculate_height(parent)
                    self.recalculate_height(right_smallest_node)
                    self.rebalance(parent)
                    self.rebalance(right_smallest_node)
            return return_val


    def inorder_traversal(self, walk):
        path = []
        stack = []
        current = walk

        while stack or current:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            path.append(current.access.id)
            current = current.right

        return path