# import example:
# import src.visualization.experiments 
# TO TEST THE MAIN SCRIPT AT THE END OF THIS FILE,
# RUN THIS FILE WITH :
# python -m src.pre_processing.output
#
# otherwise, for some reason, imports dont work (vscode run button will not find src.)

import pymongo
from typing import List

from functions import *


def get_embeddings(doc: dict) -> List[List[float]]:
    # tag = "embedding"
    return get_embedding(doc) 

def get_language(doc: dict) -> str:
    # tag = "language". Expecting "fr" or "nl"
    pass
    return

def get_source(doc: dict) -> str:
    # tag = "source". Expecting "lesoir", or "rtbf", NOT "https://www.lesoir.be"
    pass
    return

def get_sentiment(doc: dict) -> List[float]:
    # tag = "sentiment"
    pass
    return

def get_polarity(doc: dict) -> float:
    # tag = "polarity" From -1.00 to +1.00.
    pass
    return

def get_score(doc: dict) -> int:
    # tag = "cos_score"
    return cos_score(doc)

def get_data_related(doc: dict) -> int:
    # tag = "data_related". Either 1 or 0. Used as a pre-filter to simplify querying.
    return data_related(doc)
    

if __name__=="__main__":
    # Extracting one doc out of the database so you can test your function on it.
    # please check the output, they're going to run this on 3M articles.

    client = pymongo.MongoClient("mongodb://bouman:80um4N!@ec2-15-188-255-64.eu-west-3.compute.amazonaws.com:27017/")
    db = client["bouman_datatank"]
    collection = db["articles"]
    doc = collection.find_one()
    doc.update({'embeddings' : get_embeddings(doc),
                'language' : get_language(doc),
                'source' : get_source(doc),
                'sentiment' : get_sentiment(doc),
                'polarity' : get_polarity(doc),
                'data_related' : get_data_related(doc)})
    # Use doc as a test

    for key in doc:
        print(key, ": ")
        print(doc[key], '\n')


