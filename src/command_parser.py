# The CommandParser class enables validation of the command line
# arguments supplied to the setup.py and invert_index.py prgrams

import os
import re

class CommandParser:
    def __init__(self, argv):
        # initializes a new instance of the CommandParser Class
        # parameters:
        # - argv: a command line argument vector
        # returns: None
        
        self.argv = argv
        
    def get_arg(self, arg_index):
        # returns an argument based on its index in the argument vector
        # paramters:
        # - arg_index: an integer
        # returns:
        # - argument: a string
        
        return self.argv[arg_index]
    
    def validate_num_args(self, num_args):
        # raises an exception if the number of arguments in arg is not 
        # equivalent to some specified integer
        # params:
        # - num_args: an integer
        # returns: None
        
        if len(self.argv) < num_args:
            raise Exception("Command is missing arguments")
        
        elif len(self.argv) > num_args:
            raise Exception("Command has excess arguments")
        
    
    def validate_int(self, arg_index):
        # raises an exception if the specified argument is not a positive digit
        # params:
        # - num_args: an integer
        # returns: None
        
        arg = self.argv[arg_index]
        if not arg.isdigit():
            raise Exception("{} is not a valid number".format(arg))
        if int(arg) <= 0:
            raise Exception("You must return a positive number of results")
        
    def validate_file_path(self, arg_index):
        # raises an error if a specified file path does not correspond
        # to an actual file in the system
        # parameters:
        # - arg_index: an integer specifying index of the file path arg
        # returns: None
        
        path = self.argv[arg_index]
        if not os.path.isfile(path):
            raise Exception("{} is not valid file path".format(path))
        
    def validate_dir_path(self, arg_index):
        # raises an error if a specified directory path does not correspond
        # to an actual directory in the system
        # parameters:
        # - arg_index: an integer specifying index of the directory path arg
        # returns: None
        
        path = self.argv[arg_index]
        if not os.path.isdir(path):
            raise Exception("{} is not valid directory path".format(path))
        
    def validate_query(self, arg_index):
        # raises an error if a boolean query does supplied to the program
        # does not meet the appropriate constraints
        # parameters:
        # - arg_index: an integer specifying index of the query arg
        # returns: None
        
        query = self.argv[arg_index]
        
        tokens = query.split()
        
        is_phrase = False
        for token in tokens:
            if re.fullmatch(r":[\w'\u2019\u201A]+", token):
                if is_phrase:
                    raise Exception("Check colons in query. You cannot have a phrase begin within another phrase")
                else:
                    is_phrase = True
            elif re.fullmatch(r"[\w'\u2019\u201A]+:", token):
                if is_phrase:
                    is_phrase = False
                else:
                    raise Exception("Check colons in query. You cannot have a phrase end if one has not begun")
            elif re.fullmatch(r"[\w'\u2019\u201A]+", token):
                pass
            elif re.fullmatch(r":[\w'\u2019\u201A]+:", token):
                if is_phrase:
                    raise Exception("Check colons in query. You cannot have a phrase begin within another phrase")           
            else:
                raise Exception("Token {} is not recognized. Please do not use special characters".format(str(token)))
            
        if is_phrase:
            raise Exception("Phrase must be enclosed by colons")