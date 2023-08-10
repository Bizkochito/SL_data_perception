# import example:
# import src.visualization.experiments
# TO TEST THE MAIN SCRIPT AT THE END OF THIS FILE,
# RUN THIS FILE WITH :
# python -m src.pre_processing.output
#
# otherwise, for some reason, imports dont work (vscode run button will not find src.)


from typing import List
from src.pre_processing.functions import embeddings, languages, polarity, source


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
        embedding = embeddings.compute_embedding(doc)
        #print(embedding)
        source = source.get_source_url(doc)
        language = languages.language_getter(doc)
        cos_score = embeddings.cos_score(embedding)
        data_related = embeddings.data_related(cos_score)
        polarity = polarity.compute_polarity(doc,language)

        #print(counter, doc["url"])
        collection.update_one(
            {"_id": doc["_id"]},
            {
                "$set": {
                    "embedding": embedding,
                    "source": source,
                    "language": language,
                    "cos_score": cos_score,
                    "data_related": data_related,
                    "polarity": polarity,
                }
            },
        )
        # doc.update({"source": get_source(doc)})
        # doc.update({"language": get_language(doc)})
        # doc.update({"cos_score": get_score(doc)})
        # doc.update({"data_related": get_data_related(doc)})
        # doc.update({"polarity": get_polarity(doc)})
