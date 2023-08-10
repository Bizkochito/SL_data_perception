# import example:
# import src.visualization.experiments
# TO TEST THE MAIN SCRIPT AT THE END OF THIS FILE,
# RUN THIS FILE WITH :
# python -m src.pre_processing.output
#
# otherwise, for some reason, imports dont work (vscode run button will not find src.)


from typing import List
from src.pre_processing.functions import embeddings, languages, polarity, source


def get_embedding(doc: dict):
    # tag = "embedding"
    return embeddings.compute_embedding(doc)


def get_source(doc: dict):
    # tag = "source". Expecting "lesoir", or "rtbf", NOT "https://www.lesoir.be"
    return source.get_source_url(doc)


def get_language(doc: dict):
    # tag = "language". Expecting "fr" or "nl"
    return languages.language_getter(doc)


def get_polarity(doc: dict):
    # tag = "polarity" From -1.00 to +1.00.
    return polarity.compute_polarity(doc)


def get_score(doc: dict):
    # tag = "cos_score"
    return embeddings.cos_score(doc)


def get_data_related(doc: dict):
    # tag = "data_related". Either 1 or 0. Used as a pre-filter to simplify querying.
    return embeddings.data_related(doc)


if __name__ == "__main__":
    from dotenv import load_dotenv
    import pymongo
    import os

    # Extracting one doc out of the database so you can test your function on it.
    # please check the output, they're going to run this on 3M articles.
    load_dotenv()
    # print("printing mongo", os.getenv("MONGODB_URI"))
    client = pymongo.MongoClient(os.getenv("MONGODB_URI"))

    db = client["bouman_datatank"]
    collection = db["articles"]
    # docs = collection.find()

    docs = collection.find({"embedding": {"$exists": False}})
    counter = 0
    for doc in docs:
        counter += 1
        # Testing every function one by one
        print(counter, doc["url"])
        collection.update_one(
            {"_id": doc["_id"]},
            {
                "$set": {
                    "embedding": get_embedding(doc),
                    "source": get_source(doc),
                    "language": get_language(doc),
                    "cos_score": get_score(doc),
                    "data_related": get_data_related(doc),
                    "polarity": get_polarity(doc),
                }
            },
        )
        # doc.update({"source": get_source(doc)})
        # doc.update({"language": get_language(doc)})
        # doc.update({"cos_score": get_score(doc)})
        # doc.update({"data_related": get_data_related(doc)})
        # doc.update({"polarity": get_polarity(doc)})
