# Python Vector Search
This python program enables users to create an inverted index based on a set of documents, and then query for documents using keywords or phrases.

## Requirements
- python version 3.8
- pip version 22.3

## Input data format
Document can be supplied to the program as a JSON array of objects. Each object must have a "document_id" key, paired with any unique string value. The documents may have one or more other key-value pairs - the keys will be discarded and their values will be indexed and searchable.

## Usage
### Virtual environment setup
After cloning the repository, navigate to the root folder of the project.

Install virtualenv, if it is not already installed:

`python3 -m pip install --user virtualenv`

Create a new virtual environment:

`python3 -m venv env`

Activate the virtual environment:

`source env/bin/activate`

Install the needed dependencies:

`pip install -r requirements.txt`

Confirm that you are in the virtual environent by checking your python intepreter:

`which python`

Your python interpreter should be in the `env/bin` directory.

### Running the program
#### Index Creation
Before running any commands, navigate to the [src](src/) directory.

To create a new document index, run the following:

`python3 setup.py [path to json file] [path to index file]`

- The `Path to json file` argument should point to a single file that contains your set of documents.
- The `Path to index file` argument should point to a directory where the indexes will be created. If an index file already exists at this location, it will be overwritten.

Example usage: `python3 setup.py my_data/input.json my_indexes/`

#### Boolean Queries
to query an existing index, run the following:

`python3 query.py [path to index] [k] [query]`

- The `Path to index` argument should point to a directory where the indexes are stored.
- The `k` argument should be an integer specifying the maximum number of results to return.
- The `query` argumment must contain a list of one or more keywords wrapped in quotation marks

Query types:
- Keyword Queries: query terms separated by spaces (e.g. `"taylor swift music"`).
- Phrase Queries: phrases delimited by colons (e.g. `":taylor swift:"`).
- Mixed queries: a combination of phrases and keywords (e.g. `":taylor swift: music :eras tour:"`)

Example usage: `python3 query.py my_indexes/ 5 "my keywords :my phrase:"`

Note: known english-language contractions in your query will be expanded into multiple terms (e.g "you're" -> "you are").

### Leaving the virtual environment
After running the program, you can leave the virtual environment using the command:

`deactivate`