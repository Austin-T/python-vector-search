# This file contins a minimalistic implementation of a min heap for
# python

import sys
  
class MinHeap:
  
    def __init__(self, max_size):
        # initializes a new instance of the minheap class with a capacity
        # of max_size
        # params:
        # - max_size: an int
        # returns: None
        
        self.max_size = max_size
        
        self.size = 0
        self.root = 1
        
        self.heap_keys = [0]*(self.max_size + 1)
        self.heap_vals = [0]*(self.max_size + 1)
        
        self.heap_keys[0] = sys.maxsize * -1
        self.heap_vals[0] = sys.maxsize * -1
  
    def left_child(self, index):
        # returns the left child of the node at index
        # params:
        # - index: an int
        # returns:
        # - index: an int
        
        return 2 * index
  
    def right_child(self, index):
        # returns the right child of the node at index
        # params:
        # - index: an int
        # returns:
        # - index: an int        
        
        return (2 * index) + 1
    
    def parent(self, index):
        # returns parent of node at index
        # params:
        # - index: an int
        # returns:
        # - index: an int        
        
        return index//2    
  
    def is_leaf(self, index):
        # returns true if the node at index is a leaf
        # params:
        # - index: an int
        # returns:
        # - bool        
        
        return index * 2 > self.size
    
    def get_min(self):
        # returns the key.val pair at the root node
        # params: None
        # returns:
        # - key: a float
        # - val: an int
    
        key = self.heap_keys[self.root]
        val = self.heap_vals[self.root]        
        
        return key, val
    
    def get_size(self):
        # returns the size of the heap
        # params: None
        # returns:
        # - size: an int      
        
        return self.size   
               
    def swap(self, index1, index2):
        # swaps nodes at index1 and index2
        # params: None
        # returns: None  
        
        self.heap_keys[index1], self.heap_keys[index2] = self.heap_keys[index2], self.heap_keys[index1]
        self.heap_vals[index1], self.heap_vals[index2] = self.heap_vals[index2], self.heap_vals[index1]
    
    def decrease_key(self, index):
        # decreases the position of the key at index. Calls itself recursively
        # params:
        # - index: an int
        # returns: None      
  
        if not self.is_leaf(index):
            if (self.heap_keys[index] > self.heap_keys[self.left_child(index)] or 
               self.heap_keys[index] > self.heap_keys[self.right_child(index)]):
  
                if self.heap_keys[self.left_child(index)] < self.heap_keys[self.right_child(index)]:
                    self.swap(index, self.left_child(index))
                    self.decrease_key(self.left_child(index))

                else:
                    self.swap(index, self.right_child(index))
                    self.decrease_key(self.right_child(index))
  
    def insert(self, key, val):
        # inserts a node at the tiop of the heap. Removes the top node if
        # the min heap exceeds its size
        # params
        # - key: a float
        # - val: an int
        # returns: None
        
        if self.size >= self.max_size:
            self.remove()
            
        self.size += 1
        self.heap_keys[self.size] = key
        self.heap_vals[self.size] = val
  
        current = self.size
  
        while self.heap_keys[current] < self.heap_keys[self.parent(current)]:
            self.swap(current, self.parent(current))
            current = self.parent(current)

  
    def remove(self):
        # pops the top element of the heap
        # params: None
        # returns:
        # - key: a float
        # - val: an int        
  
        key = self.heap_keys[self.root]
        val = self.heap_vals[self.root]
        
        self.heap_keys[self.root] = self.heap_keys[self.size]
        self.heap_vals[self.root] = self.heap_vals[self.size]
        
        self.size -= 1
        self.decrease_key(self.root)
        
        return key, val