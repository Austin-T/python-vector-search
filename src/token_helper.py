# This file contains methods that help the create-index.py and query.py
# programs to tokenize strings and normalize tokens.

import re
import nltk
from nltk.tokenize import RegexpTokenizer

def tokenize_string(string):
    # Extracts a set of tokens from an input string.
    # params:
    # - string: a string
    # returns:
    # - tokens: a list of strings
    
    # remove any commas appearing in continous string of digits
    string = re.sub(r"(\d),(\d)", r"\1\2", string)
    
    # get tokens from any series of connected letters, numbers, and apostrophes
    tokenizer = RegexpTokenizer(r"[\w'\u2019\u201A]+")
    tokens = tokenizer.tokenize(string)
    
    return tokens

def normalize_tokens(tokens):
    # Normalizes a list of tokens using using case folding, contraction
    # expansion, and stemming. Removes any tokens from the final output
    # could not otherwise be normalized.
    # params:
    # - tokens: an list of strings
    # returns:
    # - terms: an list of strings
    
    terms = []
    for token in tokens:
        # case fold
        token = token.casefold()
        
        # expand contractions
        tokens = expand_contractions(token)
        
        for token in tokens:
            # stem words
            porter = nltk.PorterStemmer()
            term = porter.stem(token)
            
            # add to output
            terms.append(term)
        
    return terms

def expand_contractions(token):
    # Expands contractions in a token, returning a set of two tokens when
    # expansion is succesful
    # params:
    # - token: a string
    # returns:
    # - tokens: a list strings
    
    # replace apostrophe variants with standard apostrophe
    token = re.sub(r"[\u2019\u201A]", r"'", token)
    
    # ignore tokens without apostrophe
    if "'" not in token:
        return [token]
    
    # ignore tokens with apostrophe at start, end, or both
    if re.fullmatch(r"'?\w+'?", token):
        token = re.sub(r"'", "", token)
        return [token]
    
    # expand common contractions
    token = re.sub(r"can\'t", "can not", token)
    token = re.sub(r"won\'t", "will not", token)

    token = re.sub(r"\'s", " is", token)
    token = re.sub(r"\'ll", " will", token)
    token = re.sub(r"\'re", " are", token)
    token = re.sub(r"n\'t", " not", token)
    token = re.sub(r"\'d", " would", token)
    token = re.sub(r"\'ve", " have", token)
    token = re.sub(r"\'t", " not", token)
    token = re.sub(r"\'m", " am", token)
    
    # remove end of contractions that could not be expanded
    token = re.sub(r"'\w*", "", token)
    
    # return list of tokens
    return [t for t in token.split(" ") if t]
