# import example:
# from src.pre_processing import output
# or
# from src.pre_proccesing import *
# then just use your function name, **not** "src.pre_processing.myfunction()"
# good luck
# WE CANNOT SEND CODE THAT DOESNT WORK, THEY WONT KNOW
#
# RUN THIS FILE WITH YOUR CODE AND CHECK THE OUTPUT
import pymongo
from pymongo import MongoClient
from typing import List
from src.get_polarity import get_polarity

def get_embeddings(doc: dict) -> List[List[float]]:
    pass
    return 

def get_language(doc: dict) -> str:
    pass
    return

def get_source(doc: dict) -> str:
    pass
    return

def get_sentiment(doc: dict) -> List[float]:
    pass
    return

def get_polarity(doc: dict) -> float:
    pass
    return

def get_data_related(doc: dict) -> int:
    pass
    return

if __name__=="__main__":
    # Extracting one doc out of the database so you can test your function on it.
    # please check the output, they're going to run this on 3M articles.

    client = MongoClient("mongodb://bouman:80um4N!@ec2-15-188-255-64.eu-west-3.compute.amazonaws.com:27017/")
    db = client["bouman_datatank"]
    collection = db["articles"]
    doc = collection.find_one()
    # Use doc as a test
    print(type(doc)) 

