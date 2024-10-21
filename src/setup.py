# This file holds functions that orchestrate the setup.py program.
# The program accepts a json-formatted document collection as input
# and creates an inverted index and document index from it.

import sys
import nltk
import json
import math
from command_parser import CommandParser
from document import Document
from inverted_index import InvertedIndex
from document_index import DocumentIndex
from token_helper import *

def main():
    # This is the entry point for execution of the create_index program.
    # This function orchestrates the creation of an inverted index based on
    # JSON-formatted files which are supplied as input to the program by
    # the user.
    
    try:
        
        # validate the command line arguments
        parser = CommandParser(sys.argv)
        parser.validate_num_args(3)
        parser.validate_file_path(1)
        parser.validate_dir_path(2)
        
        # read in the document
        documents = load_documents(parser.get_arg(1))
        
        # tokenize and normalize the documents
        preprocess_documents(documents)
        
        # create the inverted index and document index
        inverted_index, document_index = create_indexes(documents)
        
        # save the inverted index
        save_indexes(inverted_index, document_index, parser.get_arg(2))
        
    except Exception as e:
        print("\nAn error prevented the creation of your index:\n" + str(e))
        print("\nPlease ensure your input JSON file is correctly formatted")
        print("\nExample command: python3 setup.py data/input.json indexes/\n")
    
def load_documents(file):
    # This function loads the contents of a json-formatted, UTF-8 encoded
    # file into memory, storing the infromation as a list of Document
    # objects. If any documents in the iinput file have the same IDs, the 
    # function with throw an error
    # params
    # - file: name of the json-formatted file
    # returns
    # - documents: a list of Document objects
    
    documents = []
    document_ids = set()

    # loads the contents of a UTF-8 file into memory
    with open(file, "r", encoding='utf8', errors='backslashreplace') as json_file:
        data = json.load(json_file)
        for item in data:
            document_id = None
            
            try:
                document_id = item["document_id"]
                document_id = int(document_id)
            except:
                raise Exception("Document does not contain document_id field")
            
            if document_id in document_ids:
                raise Exception("Found duplicate doc ID {}".format(document_id))
            
            document_ids.add(document_id)
            
            if len(item) > 1:
                all_data = ""
                for zone, data in item.items():
                    if zone != "document_id":
                        all_data = all_data + " " + data
                documents.append(Document(document_id, all_data))
            else:
                raise Exception("Document {} is missing zones".format(document_id))
    
    return documents
    
def preprocess_documents(documents):
    # This function converts all document data into a set of tokens, 
    # then to a set of terms belonging to equivalnece classes.
    # params:
    # - documents: a list of Document objects
    # returns:
    # - documents: a list of Document objects
    
    for document in documents:
        data = document.get_data()
        
        tokens = tokenize_string(data)
        terms = normalize_tokens(tokens)
        
        for i in range(len(terms)):
            document.add_term(terms[i], i)

def create_indexes(documents):
    # This function takes a set of documents which have already been tokenized,
    # and creates an inverted index based on the tokens and the doc IDs in
    # which they correspond
    # params:
    # - document: a list of Document objects
    # returns:
    # - dictionaries: a dict with zones as keys and Dictionary objects as values
    # - postings: a dict with zones as keys and PostingLists objects as values

    # created indexes
    inverted_index = InvertedIndex()
    document_index = DocumentIndex()

    # populate inverted index
    max_tfs = {}
    for document in documents:

        document_id = document.get_document_id()
        terms = document.get_terms()
        
        max_tf = 0
        
        for term, positions in terms.items():
            # add term to inverted index
            tf = len(positions)
            inverted_index.register_term(term, document_id, tf, positions)
            
            # update maximum document tf
            if tf > max_tf:
                max_tf = tf
                
        max_tfs[document_id] = max_tf
        
    # populate document index
    N = len(documents)
    for document in documents:
        document_id = document.get_document_id()
        terms = document.get_terms()
        
        max_tf = max_tfs[document_id]
        cos_norm_squared = 0
        
        for term, positions in terms.items():
            # calculate partial document term weight
            df = inverted_index.get_df(term)
            tf = len(positions)
            doc_df_weight = max(0, math.log((N - df)/df, 10)) # prob idf
            doc_tf_weight = 0.5 + ((0.5 * tf)/(max_tf)) # augmented tf
            doc_term_weight = doc_tf_weight * doc_df_weight
            
            # sum the square of document weights
            cos_norm_squared += doc_term_weight ** 2
            
        # recover the cosine normalization factor
        cos_norm = math.sqrt(cos_norm_squared)
        
        document_index.register_document(document_id, max_tf, cos_norm)
        
    return inverted_index, document_index

def save_indexes(inverted_index, document_index, directory):
    # This function saves an inverted index and document index as a TSV file
    # params:
    # - inverted_index: InvertedIndex object
    # - document_index: DocumentIndex object
    # - directory: a string representing the directory to save the index
    
    inverted_index.save_TSV(directory + "/" + "inverted_index.tsv")
    document_index.save_TSV(directory + "/" + "document_index.tsv")

if __name__ == '__main__':
    main()

