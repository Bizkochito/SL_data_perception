fr_sources =  ['rtbf', 'lesoir', 'dhnet', 'lalibre', 'sudinfo', 'levif', 'lavenir', 'lecho']
nl_sources =  ['tijd', 'demorgen', 'vrt', 'hln', 'knack']

def language_getter(doc):
    source = doc["source"]
    if source in fr_sources:
        return "fr"
    elif source in nl_sources:
        return "nl"
    else :
        None

