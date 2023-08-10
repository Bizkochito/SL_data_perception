from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer
from textblob_nl import PatternTagger, PatternAnalyzer

tb_fr = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
tb_nl = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

def compute_polarity(doc):
    if 'language' not in doc:
        return None
    elif doc['language'] == 'fr':
        polarity = tb_fr(doc['text']).sentiment[0]
        return polarity 
    elif doc['language'] == 'nl':
        polarity = tb_nl(doc['text']).sentiment[0]
        return polarity 
    else:
        return None