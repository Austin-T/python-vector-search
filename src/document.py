# The Document object represnts a document in the json-formatted input file.
# The Docment is used as an intermediate data structure in the creation
# of an inverted index.

from sorted_list_helper import *

class Document:
    def __init__(self, document_id, data):
        # initializes a new instance of the Document class
        # params:
        # - document_id: a string
        # - data: a string of raw data
        # returns: None
        
        self.document_id = document_id
        self.data = data
        self.tokens = {}
        self.terms = {}

    def get_document_id(self):
        # returns the document id
        # params: None
        # returns
        # - document_id: a string
        
        return self.document_id

    def get_data(self):
        # returns all data that belongs to the document
        # params: None
        # returns:
        # - text: a string
        
        return self.data
    
    def add_term(self, term, position):
        # adds a term to the set of terms. if the term already exists,
        # updates its list of positions
        # params:
        # - token: a string
        # - positions: an integer
        # returns: None
        
        if term in self.terms:
            add_to_list(position, self.terms[term])
        else:
            self.terms[term] = [ position ]

    
    def set_terms(self, terms):
        # stores a set of terms belonging to the document.
        # params:
        # - terms: a set of unique strings
        # returns: None
        
        self.terms = terms

    def get_terms(self):
        # returns all terms belonging to the document.
        # params: None
        # returns:
        # - terms: a set of unique strings
        
        return self.terms
