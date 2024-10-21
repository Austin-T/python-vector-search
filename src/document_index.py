# The DocumentIndex class represents the dictionary data structure that
# stores all document IDs, and their corresponding ____

import re

class DocumentIndex:

    max_tf = "max_tf"
    length = "length"

    def __init__(self):
        # initializes a new instance of the DocumentIndex class
        # params: None
        # returns: None
        
        self.entries = {}

    def register_document(self, document_id, max_tf, length):
        # adds a document to the dictionary but raises and error if the document
        # has aleady been added
        # params:
        # - document_id: a string
        # - max_tf: an integer
        # - length: a float
        # returns: None
        
        if document_id in self.entries:
            raise Exception("Document {} was added to index twice".format(document_id))

        else:
            self.entries[document_id] = {
                DocumentIndex.max_tf: max_tf,
                DocumentIndex.length: length
            }
    
    def get_size(self):
        # returns the number of documents in the index
        # returns:
        # - size: an int
        
        return len(self.entries)
    
    def get_document_ids(self):
        # returns every document ID
        # params: None
        # returns:
        # - document_ids: a list of strings
        
        return self.entries.keys()
    
    def get_max_tf(self, document_id):
        # returns the maximum term frequency associated with some document
        # params:
        # - document_id: a string
        # returns:
        # - max_tf: an int
        
        return self.entries[document_id][DocumentIndex.max_tf]

    def get_length(self, document_id):
        # returns the euclidian length associated with some document
        # params:
        # - document_id: a string
        # returns:
        # - length: a float
        
        return self.entries[document_id][DocumentIndex.length]

    def save_TSV(self, filename):
        # saves the DocumentIndex instance as a tab-seperated values file
        # params:
        # - filename: a string
        # returns: None
        
        with open(filename, 'w') as tsv_file:
            for document_id in sorted(self.entries):
                tsv_file.write(
                    str(document_id) + "\t" +
                    str(self.entries[document_id][DocumentIndex.max_tf]) + "\t" +
                    str(self.entries[document_id][DocumentIndex.length]) + "\n"
                )
                
    def load_TSV(self, filename):
        # loads an DocumentIndex instance from a tab-seperated values file
        # params:
        # - filename: a string
        # returns: None
        
        with open(filename, "r", encoding='utf8', errors='backslashreplace') as tsv_file:
            entries = tsv_file.readlines()
            for entry in entries:
                entry_split = entry.split("\t")
                
                document_id = int(entry_split[0])
                
                max_tf = int(entry_split[1])
                
                length = float(entry_split[2])

                self.entries[document_id] = {
                    DocumentIndex.max_tf: max_tf,
                    DocumentIndex.length: length
                }