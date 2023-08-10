from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np
embedder = SentenceTransformer("all-MiniLM-L6-v2")


def compute_embedding(doc):
    # tag = embedding
    if "text" not in doc :
        return np.array([0]*384).astype(np.float32)
    article = doc["text"]
    article_embedding = embedder.encode(article, convert_to_tensor=False)
    return article_embedding


def cos_score(embedding):
    query = [
        "database OR data reusability OR data reuse OR data sharing OR data access OR data privacy OR data protection OR GDPR"
    ]
    query_embedding = embedder.encode(query, convert_to_tensor=False)
    cos_scores = util.cos_sim(query_embedding.astype(np.float32), embedding)[0]
    return float(cos_scores.abs())


def data_related(cos_score):
    # tag = data_related
    return cos_score > 0.25

