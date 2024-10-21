# This file contains a set of helper method that enable the easy use of
# sorted lists

def add_to_list(integer, sorted_list):
    # inserts an integer into a sorted list in sorted order
    # using a binary search. The document will not be inserted into the
    # list if an identical document id already belongs to the list.
    # parameters:
    # - integer: an int
    # - sorted_list: a sorted list of strings
    # returns:
    # - success: True if document_id was added, False otherwise
    
    low = 0
    high = len(sorted_list) - 1
    
    while low <= high:
        guess = (low + high) // 2
        if sorted_list[guess] == integer:
            return False
        elif sorted_list[guess] < integer:
            low = guess + 1
        else:
            high = guess - 1
            
    sorted_list.insert(low, integer)
    
    return True
    
def add_to_mlist(list_to_add, sorted_mlist):
    # inserts a list into multidimensional list, ordered by their first element,
    # using a binary search. The document will not be inserted into the
    # list if an identical document id already belongs to the list.
    # parameters:
    # - list_to_add: a list
    # - sorted_mlist: a list of lists, sorted by the first element of each list
    # returns:
    # - success: True if document_id was added, False otherwise
    
    low = 0
    high = len(sorted_mlist) - 1
    
    while low <= high:
        guess = (low + high) // 2
        if sorted_mlist[guess][0] <= list_to_add[0]:
            low = guess + 1
        else:
            high = guess - 1
            
    sorted_mlist.insert(low, list_to_add)
    
    return True
    
def intersect_lists(list_a, list_b):
    # returns a new sorted list containing the intersection of the
    # elements in posting lists A and B (i.e. A & B)
    # parameters:
    # - list_a: a sorted list of strings
    # - list_b: a sorted list of strings
    # returns:
    # - intersection: a sorted list of strings
    
    i = 0
    j = 0
    
    intersection = []
    
    while i < len(list_a) and j < len(list_b):
        if list_a[i] == list_b[j]:
            intersection.append(list_a[i])
            i += 1
            j += 1
        elif list_a[i] < list_b[j]:
            i += 1
        else:
            j += 1
            
    return intersection
    
def intersect_mlists(list_a, list_b):
    # returns a new sorted list containing the intersection of the
    # elements in lists A and B
    # parameters:
    # - list_a: list of lists, sorted by the first element of each sub-list
    # - list_b: list of lists, sorted by the first element of each sub-list
    # returns:
    # - intersection: a list of lists
    
    i = 0
    j = 0
    
    intersection = []
    
    while i < len(list_a) and j < len(list_b):
        if list_a[i][0] == list_b[j][0]:
            intersection.append(list_a[i])
            i += 1
            j += 1
        elif list_a[i][0] < list_b[j][0]:
            i += 1
        else:
            j += 1
            
    return intersection
    
def union_lists(list_a, list_b):
    # returns a new sorted list containing the union of the
    # elements in posting lists A and B (i.e. A | B)
    # - list_a: a sorted list of strings
    # - list_b: a sorted list of strings
    # returns:
    # - union: a sorted list of strings
    
    i = 0
    j = 0
    
    union = []
    
    while i < len(list_a) and j < len(list_b):
        if list_a[i] == list_b[j]:
            union.append(list_a[i])
            i += 1
            j += 1
        elif list_a[i] < list_b[j]:
            union.append(list_a[i])
            i += 1
        else:
            union.append(list_b[j])
            j += 1
    
    while i < len(list_a):
        union.append(list_a[i])
        i += 1
        
    while j < len(list_b):
        union.append(list_b[j])
        j += 1
    
    return union
    
def union_mlists(list_a, list_b):
    # returns a new sorted list containing the union of the
    # elements in multidimensional lists A and B (i.e. A | B)
    # - list_a:  list of lists, sorted by the first element of each sub-list
    # - list_b:  list of lists, sorted by the first element of each sub-list
    # returns:
    # - union: list of lists, sorted by the first element of each sub-list
    
    i = 0
    j = 0
    
    union = []
    
    while i < len(list_a) and j < len(list_b):
        if list_a[i][0] == list_b[j][0]:
            union.append(list_a[i])
            i += 1
            j += 1
        elif list_a[i][0] < list_b[j][0]:
            union.append(list_a[i])
            i += 1
        else:
            union.append(list_b[j])
            j += 1
    
    while i < len(list_a):
        union.append(list_a[i])
        i += 1
        
    while j < len(list_b):
        union.append(list_b[j])
        j += 1
    
    return union

