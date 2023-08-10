from sentence_transformers import SentenceTransformer, util
import torch

embedder = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(doc):
    #tag = embedding 
    if "embedding" in doc :
        return None
    else :
        article = doc["text"]
        article_embedding = embedder.encode(article, convert_to_tensor=False)
    return article_embedding

def cos_score(doc):
    #tag = cos_score
    if "cos_score" in doc :
        return None
    else :
        try :
            query = ["database OR data reusability OR data reuse OR data sharing OR data access OR data privacy OR data protection OR GDPR"]
            query_embedding = embedder.encode(query, convert_to_tensor=False)
            cos_scores = util.cos_sim(query_embedding, doc["embdedding"])[0]
            return cos_scores.abs()
        except :
            return None

def data_related(doc):
    #tag = data_related
    if "data_related" in doc :
        return None
    else :
        cos_sim = doc["cos_score"]
        try:
            if cos_sim > 0.25:
                return 1
            else :
                return 0
        except : 
            return None