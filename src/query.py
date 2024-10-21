# This file holds functions that orchestrate the query.py program.
# The program accepts a file path, integer, and query as input, returning
# list of document IDs tht match the query.

import os
import sys
import re
import time
import math
from command_parser import CommandParser
from inverted_index import InvertedIndex
from document_index import DocumentIndex
from min_heap import MinHeap
from token_helper import *
from sorted_list_helper import *


def main():
    # This is the entry point for execution of the query_index program.
    # This function orchestrates the loading and querying of an inverted
    # index based on command line input.

    try:
        
        # validate the command line arguments
        parser = CommandParser(sys.argv)
        parser.validate_num_args(4)
        parser.validate_dir_path(1)
        parser.validate_int(2)
        parser.validate_query(3)
        
        # load the indexes
        inverted_index, document_index = load_indexes(parser.get_arg(1))
        
        # parse the query
        keywords, phrases = parse_query(parser.get_arg(3))
        
        # normalize the query tokens
        keywords, phrases = normalize_query(keywords, phrases)
        
        # execute the query
        document_ids = evaluate_query(
            inverted_index,
            document_index,
            keywords,
            phrases,
            int(parser.get_arg(2))
        )
    
    except Exception as e:
        print("\nAn error prevented the index from being queried:\n" + str(e))
        print("\nPlease ensure your query is correctly formatted")
        print("\nExample usage: \n"
              + "\tpython3 query.py indexes/ 5 \"Daniel Craig\"\n"
              + "\tpython3 query.py indexes/ 10 \":shaken not stirred:\"\n"
              + "\tpython3 query.py indexes/ 1 \":casino royale: james bond 007\"\n")

def load_indexes(directory):
    # This function loads inverted index and document index from the 
    # supplied directory.
    # params:
    # - directory: a string representing the directory to save the index
    # returns:
    # - inverted_index: an InvertedIndex object
    # - document_index: an DocumentIndex object
    
    inverted_file = directory + "/" + "inverted_index.tsv"
    document_file = directory + "/" + "document_index.tsv"
    
    if not os.path.exists(inverted_file):
        raise Exception("Index {} does not exist".format(inverted_file))
    
    if not os.path.exists(document_file):
        raise Exception("Index {} does not exist".format(inverted_file))    

    inverted_index = InvertedIndex()
    inverted_index.load_TSV(inverted_file)
    
    document_index = DocumentIndex()
    document_index.load_TSV(document_file)
            
    return inverted_index, document_index

def parse_query(query):
    # Parses a query string and returns a list of keywords and a list of
    # phrases contained within the string
    # params:
    # - query: a string
    # returns:
    # - keywords: a list of strings
    # - phrases: a list of lists of strings
    
    tokens = query.split()
    
    keywords = []
    phrases = []
    
    is_phrase = False
    phrase = []
    for token in tokens:
        if re.fullmatch(r":[\w'\u2019\u201A]+", token):
            is_phrase = True
            phrase.append(token[1:])
        elif re.fullmatch(r"[\w'\u2019\u201A]+:", token):
            is_phrase = False
            phrase.append(token[:-1])
            phrases.append(phrase)
            phrase = []
        elif re.fullmatch(r"[\w'\u2019\u201A]+", token):
            if is_phrase:
                phrase.append(token)
            else:
                keywords.append(token)
        elif re.fullmatch(r":[\w'\u2019\u201A]+:", token):
            phrases.append([token[1:-1]])
        else:
            raise Exception("Token {} is not recognized".format(str(token)))
        
    return keywords, phrases
    
def normalize_query(keywords, phrases):
    # Normalizes each token in the query, including keywords and phrases.
    # params:
    # - keywords: a list of strings
    # - phrases: a list of lists of strings
    # returns: None
    
    keywords_new = normalize_tokens(keywords)
    
    phrases_new = []
    for phrase in phrases:
        phrases_new.append(normalize_tokens(phrase))
            
    return keywords_new, phrases_new
        
def evaluate_query(inverted_index, document_index, keywords, phrases, k):
    # This function evaluates pre-parsed keyword and phrase queries,
    # returning a set of document IDs that match them
    # params:
    # - inverted_index: an InvertedIndex object
    # - document_index: an DocumentIndex object
    # - keywords: a list of strings
    # - phrases: a list of lists of strings
    # - k: an int
    # returns:
    # - document_ids: a list of strings
    
    # validate that there is at least one keyword or phrase
    if not keywords and not phrases:
        raise Exception("Query must contain at least one valid keyword")
    
    # create a pool of documents
    pool = []
    if phrases:
        pool = get_docs_with_phrase(inverted_index, phrases)
    else:
        pool = document_index.get_document_ids()
    
    # score each document in the pool against the query
    scored_docs = score_docs(inverted_index, document_index, keywords, phrases, pool)
    
    # find the k highest scores
    highest_docs = find_highest_docs(scored_docs, k)
    
    # print the results
    print_results(len(pool), len(scored_docs), highest_docs)

def get_docs_with_phrase(inverted_index, phrases):
    # returns a list of IDs for documents that contain any number of phrases
    # params:
    # - inverted_index: an InvertedIndex object
    # - phrases: a list of lists of strings
    # returns:
    # - document_ids: a list of strings
    
    document_ids = set()
    for phrase in phrases:
        # create a list of postings lists that contain each keyword
        
        # e.g. query ":who is you:" on dr seuss lines
        # all_postings = [
        #    [[2, 1, [14]]]
        #    [[0, 1, [10]], [2, 3, [5, 10, 15]]]
        #    [[0, 1, [3]], [2, 5, [1, 3, 16, 19, 23]], [4, 3, [2, 5, 17]]]
        # ]
        # all_postings_pointers = [
        #    0
        #    0
        #    0
        # ]
        
        all_postings = []
        all_postings_pointers = []
        
        for keyword in phrase:
            postings = inverted_index.get_postings(keyword)
            
            all_postings.append(postings)
            all_postings_pointers.append(0)
            
        # advance each pointer in the list of postings list until
        # all pointers match a single document_id
        
        # all_postings = [
        #    [[2, 1, [14]]]
        #      ^
        #    [[0, 1, [10]], [2, 3, [5, 10, 15]]]
        #                    ^
        #    [[0, 1, [3]], [2, 5, [1, 3, 16, 19, 23]], [4, 3, [2, 5, 17]]]
        #                   ^
        # ]
        # all_postings_pointers = [
        #    0
        #    1
        #    1
        # ]
        
        max_id = -1
        match = 0
        i = 0
        exhausted = False
        while not exhausted:
            i = (i + 1) % len(all_postings)
            while all_postings[i][all_postings_pointers[i]][0] < max_id:
                all_postings_pointers[i] += 1
                if all_postings_pointers[i] >= len(all_postings[i]):
                    exhausted = True
                    break
                
            if exhausted:
                break
            
            if all_postings[i][all_postings_pointers[i]][0] == max_id:
                match += 1
            else:
                max_id = all_postings[i][all_postings_pointers[i]][0]
                match = 1
                
            if match == len(all_postings):
                # a matching document_id has been found!
                match = 0
                max_id += 1
                
                # create a list of positions for a specific document_id and keyword
                
                # all_positions = [
                #    [14]
                #    [5, 10, 15]
                #    [1, 3, 16, 19, 23]
                # ]
                # all_positions_pointers = [
                #    0
                #    0
                #    0
                # ]
                # document_id = 2
                
                all_positions = []
                all_positions_pointers = []
                
                for j in range(len(all_postings)):
                    positions = all_postings[j][all_postings_pointers[j]][2]
                    
                    all_positions.append(positions)
                    all_positions_pointers.append(0)            
                
                document_id = all_postings[j][all_postings_pointers[j]][0]
                
                # advance each pointer in the list of positions lists until
                # each points to an increasing number
                
                # all_positions = [
                #    [14]
                #     ^
                #    [5, 10, 15]
                #            ^
                #    [1, 3, 16, 19, 23]
                #           ^
                # ]
                # all_positions_pointers = [
                #    0
                #    2
                #    2
                # ]
                base_num = -1
                j = 0
                match_2 = 0
                exhausted_2 = False
                while not exhausted_2:
                    j = (j + 1) % len(all_postings)
                    while all_positions[j][all_positions_pointers[j]] < base_num + j:
                        all_positions_pointers[j] += 1
                        if all_positions_pointers[j] >= len(all_positions[j]):
                            exhausted_2 = True
                            break
                        
                    if exhausted_2:
                        break
                    
                    if all_positions[j][all_positions_pointers[j]] == base_num + j:
                        match_2 += 1
                    else:
                        base_num = all_positions[j][all_positions_pointers[j]] - j
                        match_2 = 1
                        
                    if match_2 == len(all_postings):
                        # phrase has been found!
                        match_2 = 0
                        base_num += 1
                        
                        document_ids.add(document_id)
                        
                        
    return list(document_ids)

    
def score_docs(inverted_index, document_index, keywords, phrases, doc_pool):
    # scores a set of documents agains a query vector following
    # algorithm 7.1 from the information retreival textbook
    # params:
    # - inverted_index: an InvertedIndex object
    # - document_index: an DocumentIndex object
    # - keywords: a list of strings
    # - phrases: a list of lists of strings
    # - doc_pool: a list of document IDs
    # returns:
    # - scored_docs: a dictionary of document_id-score pairings
    
    # find the set of unique terms in the query. TF does not matter
    query_terms = set()
    for keyword in keywords:
        query_terms.add(keyword)
    for phrase in phrases:
        for term in phrase:
            query_terms.add(term)
    
    # initialize a dictionary to store document scores
    doc_score = {}
    for doc in doc_pool:
        doc_score[doc] = 0
        
    # score each term in the query
    N = document_index.get_size()
    
    for term in query_terms:
        # fetch postings list and df from inverted index
        postings = inverted_index.get_postings(term)
        df = inverted_index.get_df(term)
        
        # ignore term that dont belong to any documents
        if not df:
            continue
        
        # calculate query term weight
        query_tf_weight = 1 # boolean tf
        query_df_weight =  math.log(N/df, 10) # idf
        query_term_weight = query_tf_weight * query_df_weight
        
        # calculate partial document term weight
        doc_df_weight = max(0, math.log((N - df)/df, 10)) # prob idf
        
        for posting in postings:
            document_id = posting[0]
            tf = posting[1]
            
            if document_id in doc_score:
                # calculate document term weight
                max_tf = document_index.get_max_tf(document_id)
                doc_tf_weight = 0.5 + ((0.5 * tf)/(max_tf)) # augmented tf
                doc_term_weight = doc_tf_weight * doc_df_weight
                
                # score the doc & query term
                doc_score[document_id] += query_term_weight * doc_term_weight
                
    # cosine-normalize scores
    scored_docs = {}
    for document_id in doc_score.keys():
        if doc_score[document_id]:
            scored_docs[document_id] = doc_score[document_id] / document_index.get_length(document_id)
    
    return scored_docs
    
def find_highest_docs(document_ids, k):
    # params:
    # - document_ids: a dictionary of document_id-score pairings
    # - k: an int
    # returns:
    # - highest_docs: a sorted list of [document_id, score] pairings
    
    min_heap = MinHeap(k)
    
    # insert any document into the heap whos score is less than the root node
    for document_id, score in document_ids.items():
        root_score, _ = min_heap.get_min()
        if score > root_score or min_heap.get_size() < k:
            min_heap.insert(score, document_id)
            
    
    # remove all elements from heap
    highest_docs = []
    while min_heap.get_size() > 0:
        score, document_id = min_heap.remove()
        highest_docs.append([document_id, score])
    
    return highest_docs
    
def print_results(pool_size, nonzero_scores, document_ids):
    # prints a list of document_ids in sorted order for easy evaluation of
    # testing results. Prints a count of the total results found and time
    # taken during query
    # parameters:
    # - document_ids: a set of strings
    # - df: an integer
    # - time: a float
    # returns: None
    
    print("Documents considered: {}".format(pool_size))
    
    print("Documents with non-zero similarity score: {}".format(nonzero_scores))
    
    print("Doc ID\tScore")
    for document_id, score in reversed(document_ids):
        print("{}\t{}".format(document_id, score))
    
if __name__ == '__main__':
    main()

