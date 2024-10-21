# The InvertedIndex class represents the dictionary data structure that
# stores all terms, their document frequencies, and the postings lists
# the belong to them

import re
from sorted_list_helper import *

class InvertedIndex:

    postings = "postings"
    df = "df"

    def __init__(self):
        # initializes a new instance of the InvertedIndex class
        # params: None
        # returns: None
        
        self.entries = {}

    def register_term(self, term, document_id, tf, positions):
        # adds a term to the dictionary but only if the term does not already
        # exist. Increments the document frequency by one when a document_id is 
        # added to a postings list
        # params:
        # - document_id: a string
        # - term: a string
        # - positions: a list of integers
        # returns: None
        
        if term in self.entries:
            added = add_to_mlist([document_id, tf, positions], self.entries[term][InvertedIndex.postings])
            
            if added:
                self.entries[term][InvertedIndex.df] += 1

        else:
            self.entries[term] = {
                InvertedIndex.df: 1,
                InvertedIndex.postings: [ [document_id, tf, positions] ]
            }
            
    def get_postings(self, term):
        # returns the set of postings associated with some term
        # params:
        # - term: a string
        # returns:
        # - posting: a list of document_id, tf, [positions]
        
        if term in self.entries:
            return self.entries[term][InvertedIndex.postings]
        
        return []
    
    def get_df(self, term):
        # returns the document frequency associated with some term
        # params:
        # - term: a string
        # returns:
        # - df: an int
        
        if term in self.entries:
            return self.entries[term][InvertedIndex.df]
        
        return 0
    
    def get_size(self):
        # returns the vocabulary size (i.e. the number of terms in the index)
        # returns:
        # - size: an int
        
        return len(self.entries)

    def save_TSV(self, filename):
        # saves the InvertedIndex instance as a tab-seperated values file
        # params:
        # - filename: a string
        # returns: None
        
        with open(filename, 'w') as tsv_file:
            for term in sorted(self.entries):
                tsv_file.write(
                    term + "\t" +
                    str(self.entries[term][InvertedIndex.df]) + "\t" +
                    str(self.entries[term][InvertedIndex.postings]) + "\n"
                )
                
    def load_TSV(self, filename):
        # loads an InvertedIndex instance from a tab-seperated values file
        # params:
        # - filename: a string
        # returns: None
        
        with open(filename, "r", encoding='utf8', errors='backslashreplace') as tsv_file:
            entries = tsv_file.readlines()
            for entry in entries:
                entry = entry.split("\t")
                
                term = entry[0]
                df = int(entry[1])
                postings = entry[2]
                
                postings = postings.split("], [")
                for i in range(len(postings)):
                    posting = postings[i]
                    
                    if i == 0:
                        posting = posting[2:]
                    if i == len(postings) - 1:
                        posting = posting[:-3]
                    
                    posting = posting.split(", ", 2)
                    
                    document_id = int(posting[0])
                    tf = int(posting[1])
                    positions = posting[2]
                    
                    positions = positions.split(", ")
                    for j in range(len(positions)):
                        position = positions[j]
                        
                        if j == 0:
                            position = position[1:]
                        if j == len(positions) - 1:
                            position = position[:-1]
                            
                        positions[j] = int(position)
                    
                    postings[i] = [document_id, tf, positions]
                
                self.entries[term] = {
                    InvertedIndex.df: df,
                    InvertedIndex.postings: postings
                }