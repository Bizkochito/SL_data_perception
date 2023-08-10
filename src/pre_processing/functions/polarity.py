from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer
from textblob_nl import PatternTagger, PatternAnalyzer

tb_fr = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
tb_nl = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())


def compute_polarity(doc,language):
    if language is None:
        return None
    elif language == "fr" and "text" in doc:
        polarity = tb_fr(doc["text"]).sentiment[0]
        return polarity
    elif language == "nl" and "text" in doc:
        polarity = tb_nl(doc["text"]).sentiment[0]
        return polarity
    else:
        return None
